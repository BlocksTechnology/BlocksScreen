import typing
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


class BlocksCustomCheckButton(QtWidgets.QAbstractButton):
    """Custom Blocks QPushButton
        Rounded button with a hole on the left side where an icon can be inserted

    Args:
        parent (QWidget): Parent of the button
    """

    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomCheckButtonǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomCheckButtonǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_orig(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_1(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(None)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_2(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = ""
        self._text: str = ""
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_3(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_4(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = "XXXX"
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_5(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(None, True)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_6(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, None)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_7(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(True)

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_8(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, )

    def xǁBlocksCustomCheckButtonǁ__init____mutmut_9(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.button_ellipse = None
        self._text: str = ""
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, False)
    
    xǁBlocksCustomCheckButtonǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomCheckButtonǁ__init____mutmut_1': xǁBlocksCustomCheckButtonǁ__init____mutmut_1, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_2': xǁBlocksCustomCheckButtonǁ__init____mutmut_2, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_3': xǁBlocksCustomCheckButtonǁ__init____mutmut_3, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_4': xǁBlocksCustomCheckButtonǁ__init____mutmut_4, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_5': xǁBlocksCustomCheckButtonǁ__init____mutmut_5, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_6': xǁBlocksCustomCheckButtonǁ__init____mutmut_6, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_7': xǁBlocksCustomCheckButtonǁ__init____mutmut_7, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_8': xǁBlocksCustomCheckButtonǁ__init____mutmut_8, 
        'xǁBlocksCustomCheckButtonǁ__init____mutmut_9': xǁBlocksCustomCheckButtonǁ__init____mutmut_9
    }
    xǁBlocksCustomCheckButtonǁ__init____mutmut_orig.__name__ = 'xǁBlocksCustomCheckButtonǁ__init__'

    def setFlat(self, flat) -> None:
        """Disable setFlat behavior"""
        return

    def setAutoDefault(self, _):
        """Disable auto default behavior"""
        return

    def text(self) -> str:
        """returns Widget text"""
        return self._text

    def setText(self, text: str | None) -> None:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomCheckButtonǁsetText__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomCheckButtonǁsetText__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomCheckButtonǁsetText__mutmut_orig(self, text: str | None) -> None:
        """Set widget text"""
        if text is None:
            return
        self._text = text
        self.update()
        return

    def xǁBlocksCustomCheckButtonǁsetText__mutmut_1(self, text: str | None) -> None:
        """Set widget text"""
        if text is not None:
            return
        self._text = text
        self.update()
        return

    def xǁBlocksCustomCheckButtonǁsetText__mutmut_2(self, text: str | None) -> None:
        """Set widget text"""
        if text is None:
            return
        self._text = None
        self.update()
        return
    
    xǁBlocksCustomCheckButtonǁsetText__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomCheckButtonǁsetText__mutmut_1': xǁBlocksCustomCheckButtonǁsetText__mutmut_1, 
        'xǁBlocksCustomCheckButtonǁsetText__mutmut_2': xǁBlocksCustomCheckButtonǁsetText__mutmut_2
    }
    xǁBlocksCustomCheckButtonǁsetText__mutmut_orig.__name__ = 'xǁBlocksCustomCheckButtonǁsetText'

    def paintEvent(self, e: typing.Optional[QtGui.QPaintEvent]):
        args = [e]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_orig(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_1(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = None
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_2(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(None)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_3(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = None
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_4(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(None, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_5(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, None)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_6(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_7(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, )
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_8(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, False)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_9(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = None

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_10(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = None
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_11(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height * 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_12(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 6.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_13(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = None

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_14(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            None,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_15(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            None,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_16(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            None,
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_17(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            None,
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_18(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_19(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_20(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_21(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_22(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() - height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_23(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height / 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_24(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 1.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_25(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() - height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_26(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height / 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_27(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 1.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_28(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height / 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_29(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 1.4),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_30(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height / 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_31(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 1.4),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_32(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = None
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_33(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(None, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_34(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, None, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_35(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, None)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_36(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_37(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_38(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, )
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_39(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(224, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_40(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 224, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_41(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 224)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_42(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = None
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_43(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(None, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_44(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, None, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_45(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, None)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_46(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_47(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_48(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, )
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_49(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(1, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_50(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 1, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_51(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 1)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_52(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = None
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_53(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(None, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_54(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, None, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_55(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, None, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_56(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, None)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_57(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_58(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_59(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_60(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, )
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_61(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(165, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_62(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 165, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_63(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 165, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_64(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 91)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_65(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = None
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_66(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(None, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_67(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, None, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_68(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, None)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_69(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_70(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_71(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, )
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_72(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(256, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_73(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 256, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_74(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 256)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_75(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = None
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_76(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(None, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_77(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, None, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_78(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, None, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_79(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, None)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_80(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_81(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_82(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_83(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, )
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_84(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(1, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_85(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 1, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_86(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 1, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_87(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 91)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_88(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = None

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_89(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(None, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_90(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, None, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_91(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, None)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_92(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_93(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_94(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, )

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_95(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(256, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_96(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 256, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_97(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 256)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_98(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = None
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_99(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            None,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_100(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            None,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_101(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            None,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_102(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            None,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_103(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_104(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_105(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_106(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_107(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(None)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_108(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(None)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_109(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(None, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_110(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, None)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_111(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_112(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, )

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_113(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(None)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_114(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(None)
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_115(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont(None, 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_116(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", None))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_117(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont(14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_118(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", ))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_119(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("XXMomcakeXX", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_120(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_121(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("MOMCAKE", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_122(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 15))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_123(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                None,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_124(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                None,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_125(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                None,
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_126(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_127(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                str(self.text()),
            )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_128(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                )

    def xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_129(self, e: typing.Optional[QtGui.QPaintEvent]):
        """Re-implemented method, paint widget, optimized for performance."""

        painter = QtGui.QPainter(self)
        rect_f = self.rect().toRectF().normalized()
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        height = rect_f.height()

        radius = height / 5.0
        self.button_ellipse = QtCore.QRectF(
            rect_f.left() + height * 0.05,
            rect_f.top() + height * 0.05,
            (height * 0.40),
            (height * 0.40),
        )

        if self.isChecked():
            bg_color = QtGui.QColor(223, 223, 223)
            text_color = QtGui.QColor(0, 0, 0)
        elif self.isDown():
            bg_color = QtGui.QColor(164, 164, 164, 90)
            text_color = QtGui.QColor(255, 255, 255)
        else:
            bg_color = QtGui.QColor(0, 0, 0, 90)
            text_color = QtGui.QColor(255, 255, 255)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            rect_f,
            radius,
            radius,
            QtCore.Qt.SizeMode.AbsoluteSize,
        )

        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.fillPath(path, bg_color)

        if self.text():
            painter.setPen(text_color)
            painter.setFont(QtGui.QFont("Momcake", 14))
            painter.drawText(
                rect_f,
                QtCore.Qt.AlignmentFlag.AlignCenter,
                str(None),
            )
    
    xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_1': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_1, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_2': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_2, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_3': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_3, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_4': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_4, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_5': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_5, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_6': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_6, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_7': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_7, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_8': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_8, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_9': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_9, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_10': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_10, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_11': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_11, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_12': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_12, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_13': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_13, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_14': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_14, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_15': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_15, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_16': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_16, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_17': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_17, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_18': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_18, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_19': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_19, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_20': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_20, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_21': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_21, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_22': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_22, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_23': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_23, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_24': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_24, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_25': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_25, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_26': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_26, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_27': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_27, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_28': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_28, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_29': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_29, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_30': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_30, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_31': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_31, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_32': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_32, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_33': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_33, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_34': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_34, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_35': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_35, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_36': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_36, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_37': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_37, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_38': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_38, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_39': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_39, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_40': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_40, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_41': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_41, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_42': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_42, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_43': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_43, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_44': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_44, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_45': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_45, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_46': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_46, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_47': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_47, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_48': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_48, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_49': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_49, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_50': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_50, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_51': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_51, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_52': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_52, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_53': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_53, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_54': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_54, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_55': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_55, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_56': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_56, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_57': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_57, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_58': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_58, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_59': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_59, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_60': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_60, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_61': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_61, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_62': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_62, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_63': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_63, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_64': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_64, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_65': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_65, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_66': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_66, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_67': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_67, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_68': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_68, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_69': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_69, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_70': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_70, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_71': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_71, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_72': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_72, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_73': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_73, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_74': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_74, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_75': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_75, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_76': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_76, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_77': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_77, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_78': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_78, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_79': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_79, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_80': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_80, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_81': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_81, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_82': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_82, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_83': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_83, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_84': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_84, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_85': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_85, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_86': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_86, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_87': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_87, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_88': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_88, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_89': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_89, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_90': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_90, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_91': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_91, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_92': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_92, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_93': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_93, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_94': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_94, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_95': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_95, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_96': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_96, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_97': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_97, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_98': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_98, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_99': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_99, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_100': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_100, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_101': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_101, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_102': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_102, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_103': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_103, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_104': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_104, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_105': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_105, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_106': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_106, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_107': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_107, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_108': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_108, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_109': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_109, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_110': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_110, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_111': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_111, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_112': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_112, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_113': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_113, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_114': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_114, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_115': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_115, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_116': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_116, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_117': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_117, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_118': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_118, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_119': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_119, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_120': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_120, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_121': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_121, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_122': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_122, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_123': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_123, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_124': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_124, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_125': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_125, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_126': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_126, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_127': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_127, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_128': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_128, 
        'xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_129': xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_129
    }
    xǁBlocksCustomCheckButtonǁpaintEvent__mutmut_orig.__name__ = 'xǁBlocksCustomCheckButtonǁpaintEvent'
