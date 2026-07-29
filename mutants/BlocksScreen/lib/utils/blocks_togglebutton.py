from lib.utils.blocks_label import BlocksLabel
from lib.utils.toggleAnimatedButton import ToggleAnimatedButton
from PyQt6 import QtCore, QtGui, QtWidgets
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class NetworkWidgetbuttons(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_orig(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_1(self, parent):
        super(NetworkWidgetbuttons, self).__init__(None)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_2(self, parent):
        super(None, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_3(self, parent):
        super(NetworkWidgetbuttons, None).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_4(self, parent):
        super(self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_5(self, parent):
        super(NetworkWidgetbuttons, ).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_6(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(None)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_7(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = ""
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_8(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = ""
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_9(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = None
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_10(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "XXla testXX"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_11(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "LA TEST"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_12(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = None

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_13(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            None
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_14(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            "XX:/filament_related/media/btn_icons/filament_sensor_turn_on.svgXX"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_15(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/FILAMENT_RELATED/MEDIA/BTN_ICONS/FILAMENT_SENSOR_TURN_ON.SVG"
        )

        self._setupUI()
        self.tb = self.toggle_button

    def xǁNetworkWidgetbuttonsǁ__init____mutmut_16(self, parent):
        super(NetworkWidgetbuttons, self).__init__(parent)

        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self._icon_label = None
        self._text_label = None
        self._text: str = "la test"
        self.icon_pixmap_fp: QtGui.QPixmap = QtGui.QPixmap(
            ":/filament_related/media/btn_icons/filament_sensor_turn_on.svg"
        )

        self._setupUI()
        self.tb = None
    
    xǁNetworkWidgetbuttonsǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkWidgetbuttonsǁ__init____mutmut_1': xǁNetworkWidgetbuttonsǁ__init____mutmut_1, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_2': xǁNetworkWidgetbuttonsǁ__init____mutmut_2, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_3': xǁNetworkWidgetbuttonsǁ__init____mutmut_3, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_4': xǁNetworkWidgetbuttonsǁ__init____mutmut_4, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_5': xǁNetworkWidgetbuttonsǁ__init____mutmut_5, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_6': xǁNetworkWidgetbuttonsǁ__init____mutmut_6, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_7': xǁNetworkWidgetbuttonsǁ__init____mutmut_7, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_8': xǁNetworkWidgetbuttonsǁ__init____mutmut_8, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_9': xǁNetworkWidgetbuttonsǁ__init____mutmut_9, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_10': xǁNetworkWidgetbuttonsǁ__init____mutmut_10, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_11': xǁNetworkWidgetbuttonsǁ__init____mutmut_11, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_12': xǁNetworkWidgetbuttonsǁ__init____mutmut_12, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_13': xǁNetworkWidgetbuttonsǁ__init____mutmut_13, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_14': xǁNetworkWidgetbuttonsǁ__init____mutmut_14, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_15': xǁNetworkWidgetbuttonsǁ__init____mutmut_15, 
        'xǁNetworkWidgetbuttonsǁ__init____mutmut_16': xǁNetworkWidgetbuttonsǁ__init____mutmut_16
    }
    xǁNetworkWidgetbuttonsǁ__init____mutmut_orig.__name__ = 'xǁNetworkWidgetbuttonsǁ__init__'

    def text(self) -> str:
        """Button text"""
        return self._text

    def setText(self, new_text) -> None:
        args = [new_text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁsetText__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁsetText__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkWidgetbuttonsǁsetText__mutmut_orig(self, new_text) -> None:
        """Set widget text"""
        if self._text_label is not None:
            self._text_label.setText(f"{new_text}")
            self._text = new_text

    def xǁNetworkWidgetbuttonsǁsetText__mutmut_1(self, new_text) -> None:
        """Set widget text"""
        if self._text_label is None:
            self._text_label.setText(f"{new_text}")
            self._text = new_text

    def xǁNetworkWidgetbuttonsǁsetText__mutmut_2(self, new_text) -> None:
        """Set widget text"""
        if self._text_label is not None:
            self._text_label.setText(None)
            self._text = new_text

    def xǁNetworkWidgetbuttonsǁsetText__mutmut_3(self, new_text) -> None:
        """Set widget text"""
        if self._text_label is not None:
            self._text_label.setText(f"{new_text}")
            self._text = None
    
    xǁNetworkWidgetbuttonsǁsetText__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkWidgetbuttonsǁsetText__mutmut_1': xǁNetworkWidgetbuttonsǁsetText__mutmut_1, 
        'xǁNetworkWidgetbuttonsǁsetText__mutmut_2': xǁNetworkWidgetbuttonsǁsetText__mutmut_2, 
        'xǁNetworkWidgetbuttonsǁsetText__mutmut_3': xǁNetworkWidgetbuttonsǁsetText__mutmut_3
    }
    xǁNetworkWidgetbuttonsǁsetText__mutmut_orig.__name__ = 'xǁNetworkWidgetbuttonsǁsetText'

    def setPixmap(self, pixmap: QtGui.QPixmap):
        args = [pixmap]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_orig(self, pixmap: QtGui.QPixmap):
        """Set widget pixmap"""
        self.icon_pixmap_fp = pixmap

    def xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_1(self, pixmap: QtGui.QPixmap):
        """Set widget pixmap"""
        self.icon_pixmap_fp = None
    
    xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_1': xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_1
    }
    xǁNetworkWidgetbuttonsǁsetPixmap__mutmut_orig.__name__ = 'xǁNetworkWidgetbuttonsǁsetPixmap'

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_orig(self, event: QtGui.QMouseEvent):
        """Re-implemented method, handle mouse press events"""
        if self.toggle_button.geometry().contains(event.pos()):
            event.ignore()
            return
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        event.accept()

    def xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_1(self, event: QtGui.QMouseEvent):
        """Re-implemented method, handle mouse press events"""
        if self.toggle_button.geometry().contains(None):
            event.ignore()
            return
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        event.accept()

    def xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_2(self, event: QtGui.QMouseEvent):
        """Re-implemented method, handle mouse press events"""
        if self.toggle_button.geometry().contains(event.pos()):
            event.ignore()
            return
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
        event.accept()
    
    xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_1': xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_1, 
        'xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_2': xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_2
    }
    xǁNetworkWidgetbuttonsǁmousePressEvent__mutmut_orig.__name__ = 'xǁNetworkWidgetbuttonsǁmousePressEvent'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = None
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(None)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(None, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, None)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, )
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, False)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            None, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, None
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, False
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            None, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, None
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, False
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = None
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(None, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, None, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, None, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, None)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, )
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(14, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 100, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 129, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 55)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = None

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(None, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, None, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, None, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, None)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, )

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(256, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 256, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 256, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 55)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_44(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = None
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_45(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(None)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_46(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(None)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_47(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = None
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_48(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(None)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_49(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(None)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_50(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = None
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_51(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            None,
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_52(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            None,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_53(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            None,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_54(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            None,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_55(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_56(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_57(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_58(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_59(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            16,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_60(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            16,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_61(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(None)
        style_painter.fillPath(background_rect, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_62(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(None, _brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_63(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, None)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_64(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(_brush)
        style_painter.end()

    def xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_65(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        style_painter = QtWidgets.QStylePainter(self)
        style_painter.setRenderHint(style_painter.RenderHint.Antialiasing, True)
        style_painter.setRenderHint(
            style_painter.RenderHint.SmoothPixmapTransform, True
        )
        style_painter.setRenderHint(
            style_painter.RenderHint.LosslessImageRendering, True
        )
        if self.isEnabled():
            _color = QtGui.QColor(13, 99, 128, 54)
        else:
            _color = QtGui.QColor(255, 255, 255, 54)

        _brush = QtGui.QBrush()
        _brush.setColor(_color)

        _brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        pen = style_painter.pen()
        pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        if self._icon_label:
            self._icon_label.setPixmap(self.icon_pixmap_fp)
        background_rect = QtGui.QPainterPath()
        background_rect.addRoundedRect(
            self.contentsRect().toRectF(),
            15,
            15,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )
        style_painter.setBrush(_brush)
        style_painter.fillPath(background_rect, )
        style_painter.end()
    
    xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_1': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_1, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_2': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_2, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_3': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_3, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_4': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_4, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_5': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_5, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_6': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_6, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_7': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_7, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_8': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_8, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_9': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_9, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_10': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_10, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_11': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_11, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_12': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_12, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_13': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_13, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_14': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_14, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_15': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_15, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_16': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_16, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_17': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_17, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_18': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_18, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_19': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_19, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_20': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_20, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_21': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_21, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_22': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_22, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_23': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_23, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_24': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_24, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_25': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_25, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_26': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_26, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_27': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_27, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_28': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_28, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_29': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_29, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_30': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_30, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_31': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_31, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_32': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_32, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_33': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_33, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_34': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_34, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_35': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_35, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_36': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_36, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_37': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_37, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_38': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_38, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_39': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_39, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_40': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_40, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_41': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_41, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_42': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_42, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_43': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_43, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_44': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_44, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_45': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_45, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_46': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_46, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_47': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_47, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_48': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_48, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_49': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_49, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_50': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_50, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_51': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_51, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_52': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_52, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_53': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_53, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_54': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_54, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_55': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_55, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_56': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_56, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_57': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_57, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_58': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_58, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_59': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_59, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_60': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_60, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_61': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_61, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_62': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_62, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_63': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_63, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_64': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_64, 
        'xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_65': xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_65
    }
    xǁNetworkWidgetbuttonsǁpaintEvent__mutmut_orig.__name__ = 'xǁNetworkWidgetbuttonsǁpaintEvent'

    def setDisabled(self, a0: bool) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_orig(self, a0: bool) -> None:
        """Re-implemented method, disable widget"""
        self.toggle_button.setDisabled(a0)
        self.repaint()
        self.toggle_button.repaint()
        return super().setDisabled(a0)

    def xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_1(self, a0: bool) -> None:
        """Re-implemented method, disable widget"""
        self.toggle_button.setDisabled(None)
        self.repaint()
        self.toggle_button.repaint()
        return super().setDisabled(a0)

    def xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_2(self, a0: bool) -> None:
        """Re-implemented method, disable widget"""
        self.toggle_button.setDisabled(a0)
        self.repaint()
        self.toggle_button.repaint()
        return super().setDisabled(None)
    
    xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_1': xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_1, 
        'xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_2': xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_2
    }
    xǁNetworkWidgetbuttonsǁsetDisabled__mutmut_orig.__name__ = 'xǁNetworkWidgetbuttonsǁsetDisabled'

    def _setupUI(self):
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_orig'), object.__getattribute__(self, 'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_mutants'), args, kwargs, self)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_orig(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_1(self):
        _policy = None
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_2(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = None
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_3(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(None, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_4(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, None)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_5(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_6(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, )
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_7(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(None)
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_8(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(None)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_9(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = None
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_10(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(None)
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_11(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName(None)
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_12(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("XXsensorHorizontalLayoutXX")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_13(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorhorizontallayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_14(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("SENSORHORIZONTALLAYOUT")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_15(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = None
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_16(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(None)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_17(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(None)
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_18(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(None)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_19(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(None, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_20(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, None)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_21(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_22(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, )
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_23(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(61, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_24(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 61)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_25(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(None, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_26(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, None)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_27(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_28(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, )
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_29(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(61, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_30(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 61)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_31(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(None)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_32(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(None)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_33(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = None
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_34(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=None)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_35(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(None)
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_36(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(None, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_37(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, None)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_38(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_39(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, )
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_40(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(101, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_41(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 61)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_42(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(None, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_43(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, None)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_44(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_45(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, )
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_46(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(501, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_47(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 61)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_48(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = None
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_49(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(None)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_50(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(None)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_51(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(19)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_52(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = None
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_53(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(None, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_54(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, None)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_55(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_56(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, )
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_57(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(None)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_58(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(None)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_59(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(None)
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_60(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(None))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_61(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(None)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_62(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = None
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_63(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(None)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_64(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(None)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_65(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(71)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_66(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(None)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_67(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(71)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_68(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(None)
        self.setLayout(self.sensor_horizontal_layout)

    def xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_69(self):
        _policy = QtWidgets.QSizePolicy.Policy.MinimumExpanding
        size_policy = QtWidgets.QSizePolicy(_policy, _policy)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.sensor_horizontal_layout = QtWidgets.QHBoxLayout()
        self.sensor_horizontal_layout.setGeometry(self.rect())
        self.sensor_horizontal_layout.setObjectName("sensorHorizontalLayout")
        self._icon_label = BlocksLabel(self)
        size_policy.setHeightForWidth(self._icon_label.sizePolicy().hasHeightForWidth())
        self._icon_label.setSizePolicy(size_policy)
        self._icon_label.setMinimumSize(60, 60)
        self._icon_label.setMaximumSize(60, 60)
        self._icon_label.setPixmap(self.icon_pixmap_fp)
        self.sensor_horizontal_layout.addWidget(self._icon_label)
        self._text_label = QtWidgets.QLabel(parent=self)
        size_policy.setHeightForWidth(self._text_label.sizePolicy().hasHeightForWidth())
        self._text_label.setMinimumSize(100, 60)
        self._text_label.setMaximumSize(500, 60)
        _font = QtGui.QFont()
        _font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        _font.setPointSize(18)
        palette = self._text_label.palette()
        palette.setColor(palette.ColorRole.WindowText, QtGui.QColorConstants.White)
        self._text_label.setPalette(palette)
        self._text_label.setFont(_font)
        self._text_label.setText(str(self._text))
        self.sensor_horizontal_layout.addWidget(self._text_label)
        self.toggle_button = ToggleAnimatedButton(self)
        self.toggle_button.setMinimumWidth(70)
        self.toggle_button.setMaximumHeight(70)
        self.sensor_horizontal_layout.addWidget(self.toggle_button)
        self.setLayout(None)
    
    xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_1': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_1, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_2': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_2, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_3': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_3, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_4': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_4, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_5': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_5, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_6': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_6, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_7': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_7, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_8': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_8, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_9': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_9, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_10': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_10, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_11': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_11, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_12': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_12, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_13': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_13, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_14': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_14, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_15': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_15, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_16': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_16, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_17': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_17, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_18': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_18, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_19': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_19, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_20': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_20, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_21': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_21, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_22': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_22, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_23': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_23, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_24': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_24, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_25': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_25, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_26': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_26, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_27': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_27, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_28': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_28, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_29': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_29, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_30': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_30, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_31': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_31, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_32': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_32, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_33': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_33, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_34': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_34, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_35': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_35, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_36': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_36, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_37': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_37, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_38': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_38, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_39': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_39, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_40': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_40, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_41': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_41, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_42': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_42, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_43': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_43, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_44': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_44, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_45': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_45, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_46': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_46, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_47': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_47, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_48': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_48, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_49': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_49, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_50': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_50, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_51': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_51, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_52': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_52, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_53': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_53, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_54': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_54, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_55': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_55, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_56': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_56, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_57': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_57, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_58': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_58, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_59': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_59, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_60': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_60, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_61': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_61, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_62': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_62, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_63': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_63, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_64': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_64, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_65': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_65, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_66': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_66, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_67': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_67, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_68': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_68, 
        'xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_69': xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_69
    }
    xǁNetworkWidgetbuttonsǁ_setupUI__mutmut_orig.__name__ = 'xǁNetworkWidgetbuttonsǁ_setupUI'
