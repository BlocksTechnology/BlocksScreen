from PyQt6 import QtCore, QtGui, QtWidgets
import typing
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


class BlocksCustomFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomFrameǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomFrameǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁBlocksCustomFrameǁ__init____mutmut_orig(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_1(self, parent=None):
        super().__init__(None)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_2(self, parent=None):
        super().__init__(parent)

        self._radius = None
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_3(self, parent=None):
        super().__init__(parent)

        self._radius = 11
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_4(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = None
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_5(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 16
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_6(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = None
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_7(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = True
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_8(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = None

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_9(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = "XXXX"

        self.setMinimumHeight(40)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_10(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(None)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_11(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(41)
        self.setMinimumWidth(300)
    def xǁBlocksCustomFrameǁ__init____mutmut_12(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(None)
    def xǁBlocksCustomFrameǁ__init____mutmut_13(self, parent=None):
        super().__init__(parent)

        self._radius = 10
        self._left_line_width = 15
        self._is_centered = False
        self.text = ""

        self.setMinimumHeight(40)
        self.setMinimumWidth(301)
    
    xǁBlocksCustomFrameǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomFrameǁ__init____mutmut_1': xǁBlocksCustomFrameǁ__init____mutmut_1, 
        'xǁBlocksCustomFrameǁ__init____mutmut_2': xǁBlocksCustomFrameǁ__init____mutmut_2, 
        'xǁBlocksCustomFrameǁ__init____mutmut_3': xǁBlocksCustomFrameǁ__init____mutmut_3, 
        'xǁBlocksCustomFrameǁ__init____mutmut_4': xǁBlocksCustomFrameǁ__init____mutmut_4, 
        'xǁBlocksCustomFrameǁ__init____mutmut_5': xǁBlocksCustomFrameǁ__init____mutmut_5, 
        'xǁBlocksCustomFrameǁ__init____mutmut_6': xǁBlocksCustomFrameǁ__init____mutmut_6, 
        'xǁBlocksCustomFrameǁ__init____mutmut_7': xǁBlocksCustomFrameǁ__init____mutmut_7, 
        'xǁBlocksCustomFrameǁ__init____mutmut_8': xǁBlocksCustomFrameǁ__init____mutmut_8, 
        'xǁBlocksCustomFrameǁ__init____mutmut_9': xǁBlocksCustomFrameǁ__init____mutmut_9, 
        'xǁBlocksCustomFrameǁ__init____mutmut_10': xǁBlocksCustomFrameǁ__init____mutmut_10, 
        'xǁBlocksCustomFrameǁ__init____mutmut_11': xǁBlocksCustomFrameǁ__init____mutmut_11, 
        'xǁBlocksCustomFrameǁ__init____mutmut_12': xǁBlocksCustomFrameǁ__init____mutmut_12, 
        'xǁBlocksCustomFrameǁ__init____mutmut_13': xǁBlocksCustomFrameǁ__init____mutmut_13
    }
    xǁBlocksCustomFrameǁ__init____mutmut_orig.__name__ = 'xǁBlocksCustomFrameǁ__init__'

    def setRadius(self, radius: int):
        args = [radius]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetRadius__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetRadius__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomFrameǁsetRadius__mutmut_orig(self, radius: int):
        """Set widget frame radius"""
        self._radius = radius
        self.update()

    def xǁBlocksCustomFrameǁsetRadius__mutmut_1(self, radius: int):
        """Set widget frame radius"""
        self._radius = None
        self.update()
    
    xǁBlocksCustomFrameǁsetRadius__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomFrameǁsetRadius__mutmut_1': xǁBlocksCustomFrameǁsetRadius__mutmut_1
    }
    xǁBlocksCustomFrameǁsetRadius__mutmut_orig.__name__ = 'xǁBlocksCustomFrameǁsetRadius'

    def setLeftLineWidth(self, width: int):
        args = [width]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_orig(self, width: int):
        """Set widget left line  width"""
        self._left_line_width = width
        self.update()

    def xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_1(self, width: int):
        """Set widget left line  width"""
        self._left_line_width = None
        self.update()
    
    xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_1': xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_1
    }
    xǁBlocksCustomFrameǁsetLeftLineWidth__mutmut_orig.__name__ = 'xǁBlocksCustomFrameǁsetLeftLineWidth'

    def setCentered(self, centered: bool):
        args = [centered]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetCentered__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetCentered__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomFrameǁsetCentered__mutmut_orig(self, centered: bool):
        """Set if text is centered or left-aligned"""
        self._is_centered = centered
        self.update()

    def xǁBlocksCustomFrameǁsetCentered__mutmut_1(self, centered: bool):
        """Set if text is centered or left-aligned"""
        self._is_centered = None
        self.update()
    
    xǁBlocksCustomFrameǁsetCentered__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomFrameǁsetCentered__mutmut_1': xǁBlocksCustomFrameǁsetCentered__mutmut_1
    }
    xǁBlocksCustomFrameǁsetCentered__mutmut_orig.__name__ = 'xǁBlocksCustomFrameǁsetCentered'

    def setProperty(self, name: str | None, value: typing.Any) -> bool:
        args = [name, value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetProperty__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomFrameǁsetProperty__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_orig(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_1(self, name: str | None, value: typing.Any) -> bool:
        if name != "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_2(self, name: str | None, value: typing.Any) -> bool:
        if name == "XXtextXX":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_3(self, name: str | None, value: typing.Any) -> bool:
        if name == "TEXT":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_4(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = None
            self.update()
            return True
        return super().setProperty(name, value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_5(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return False
        return super().setProperty(name, value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_6(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(None, value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_7(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, None)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_8(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(value)

    def xǁBlocksCustomFrameǁsetProperty__mutmut_9(self, name: str | None, value: typing.Any) -> bool:
        if name == "text":
            self.text = value
            self.update()
            return True
        return super().setProperty(name, )
    
    xǁBlocksCustomFrameǁsetProperty__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomFrameǁsetProperty__mutmut_1': xǁBlocksCustomFrameǁsetProperty__mutmut_1, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_2': xǁBlocksCustomFrameǁsetProperty__mutmut_2, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_3': xǁBlocksCustomFrameǁsetProperty__mutmut_3, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_4': xǁBlocksCustomFrameǁsetProperty__mutmut_4, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_5': xǁBlocksCustomFrameǁsetProperty__mutmut_5, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_6': xǁBlocksCustomFrameǁsetProperty__mutmut_6, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_7': xǁBlocksCustomFrameǁsetProperty__mutmut_7, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_8': xǁBlocksCustomFrameǁsetProperty__mutmut_8, 
        'xǁBlocksCustomFrameǁsetProperty__mutmut_9': xǁBlocksCustomFrameǁsetProperty__mutmut_9
    }
    xǁBlocksCustomFrameǁsetProperty__mutmut_orig.__name__ = 'xǁBlocksCustomFrameǁsetProperty'

    def paintEvent(self, a0):
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomFrameǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomFrameǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_orig(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_1(self, a0):
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_2(self, a0):
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_3(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_4(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = None
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_5(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(None)
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_6(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = None
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_7(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(None)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_8(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(None, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_9(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, None, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_10(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, None, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_11(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, None))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_12(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_13(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_14(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_15(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, ))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_16(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(21, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_17(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 21, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_18(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 21, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_19(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 71))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_20(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(None)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_21(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_22(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(None)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_23(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(None)
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_24(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(None))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_25(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(None, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_26(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, None, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_27(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, None, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_28(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, None)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_29(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_30(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_31(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_32(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, )))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_33(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(51, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_34(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 51, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_35(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 51, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_36(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 101)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_37(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(None, self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_38(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), None, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_39(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, None)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_40(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_41(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_42(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, )

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_43(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(None, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_44(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, None, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_45(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, None, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_46(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, None), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_47(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_48(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_49(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_50(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, ), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_51(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(2, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_52(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 2, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_53(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, +1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_54(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -2, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_55(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, +1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_56(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -2), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_57(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(None)
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_58(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor(None))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_59(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("XXwhiteXX"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_60(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("WHITE"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_61(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = None
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_62(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(None)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_63(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(13)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_64(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(None)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_65(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = None
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_66(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = None
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_67(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(None)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_68(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = None

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_69(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = None
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_70(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 11
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_71(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = None
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_72(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 9
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_73(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = None

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_74(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin - baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_75(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline / 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_76(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 3

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_77(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = None
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_78(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = None

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_79(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = None

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_80(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing - right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_81(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width - spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_82(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing - text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_83(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width - spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_84(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = None
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_85(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) / 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_86(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() + total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_87(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 3
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_88(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = None

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_89(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(None, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_90(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, None)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_91(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_92(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, )

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_93(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = None
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_94(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = None
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_95(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = None

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_96(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 1

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_97(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = None
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_98(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(None, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_99(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, None, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_100(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, None, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_101(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, None)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_102(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_103(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_104(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_105(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, )
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_106(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y + 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_107(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 2, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_108(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 4)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_109(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(None, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_110(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, None)
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_111(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_112(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, )
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_113(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor(None))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_114(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("XXwhiteXX"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_115(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("WHITE"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_116(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x = left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_117(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x -= left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_118(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width - spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_119(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(None, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_120(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, None, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_121(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, None)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_122(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_123(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_124(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, )
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_125(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin - baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_126(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x = text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_127(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x -= text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_128(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width - spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_129(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = None
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_130(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = None
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_131(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x + margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_132(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() + x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_133(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = None

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_134(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(None, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_135(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, None)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_136(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_137(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, )

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_138(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(1, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_139(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = None

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_140(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(None, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_141(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, None, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_142(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, None, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_143(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, None)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_144(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_145(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_146(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_147(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, )

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_148(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y + 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_149(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 2, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_150(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 4)

            painter.fillRect(big_rect, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_151(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(None, QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_152(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, None)

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_153(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(QtGui.QColor("white"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_154(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, )

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_155(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor(None))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_156(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("XXwhiteXX"))

    def xǁBlocksCustomFrameǁpaintEvent__mutmut_157(self, a0):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20, 70))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(50, 50, 50, 100)))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), self._radius, self._radius)

        if self.text:
            painter.setPen(QtGui.QColor("white"))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.text)
            baseline = fm.ascent()

            margin = 10
            spacing = 8
            line_center_y = margin + baseline // 2

            if self._is_centered:
                left_line_width = self._left_line_width
                right_line_width = self._left_line_width

                total_content_width = (
                    left_line_width + spacing + text_width + spacing + right_line_width
                )

                start_x = (self.width() - total_content_width) // 2
                x = max(margin, start_x)

            else:
                left_line_width = self._left_line_width
                x = margin
                right_line_width = 0

            small_rect = QtCore.QRect(x, line_center_y - 1, left_line_width, 3)
            painter.fillRect(small_rect, QtGui.QColor("white"))
            x += left_line_width + spacing

            painter.drawText(x, margin + baseline, self.text)
            x += text_width + spacing

            if self._is_centered:
                big_rect_width = right_line_width
            else:
                remaining_width = self.width() - x - margin
                big_rect_width = max(0, remaining_width)

            big_rect = QtCore.QRect(x, line_center_y - 1, big_rect_width, 3)

            painter.fillRect(big_rect, QtGui.QColor("WHITE"))
    
    xǁBlocksCustomFrameǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomFrameǁpaintEvent__mutmut_1': xǁBlocksCustomFrameǁpaintEvent__mutmut_1, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_2': xǁBlocksCustomFrameǁpaintEvent__mutmut_2, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_3': xǁBlocksCustomFrameǁpaintEvent__mutmut_3, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_4': xǁBlocksCustomFrameǁpaintEvent__mutmut_4, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_5': xǁBlocksCustomFrameǁpaintEvent__mutmut_5, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_6': xǁBlocksCustomFrameǁpaintEvent__mutmut_6, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_7': xǁBlocksCustomFrameǁpaintEvent__mutmut_7, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_8': xǁBlocksCustomFrameǁpaintEvent__mutmut_8, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_9': xǁBlocksCustomFrameǁpaintEvent__mutmut_9, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_10': xǁBlocksCustomFrameǁpaintEvent__mutmut_10, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_11': xǁBlocksCustomFrameǁpaintEvent__mutmut_11, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_12': xǁBlocksCustomFrameǁpaintEvent__mutmut_12, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_13': xǁBlocksCustomFrameǁpaintEvent__mutmut_13, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_14': xǁBlocksCustomFrameǁpaintEvent__mutmut_14, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_15': xǁBlocksCustomFrameǁpaintEvent__mutmut_15, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_16': xǁBlocksCustomFrameǁpaintEvent__mutmut_16, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_17': xǁBlocksCustomFrameǁpaintEvent__mutmut_17, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_18': xǁBlocksCustomFrameǁpaintEvent__mutmut_18, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_19': xǁBlocksCustomFrameǁpaintEvent__mutmut_19, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_20': xǁBlocksCustomFrameǁpaintEvent__mutmut_20, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_21': xǁBlocksCustomFrameǁpaintEvent__mutmut_21, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_22': xǁBlocksCustomFrameǁpaintEvent__mutmut_22, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_23': xǁBlocksCustomFrameǁpaintEvent__mutmut_23, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_24': xǁBlocksCustomFrameǁpaintEvent__mutmut_24, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_25': xǁBlocksCustomFrameǁpaintEvent__mutmut_25, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_26': xǁBlocksCustomFrameǁpaintEvent__mutmut_26, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_27': xǁBlocksCustomFrameǁpaintEvent__mutmut_27, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_28': xǁBlocksCustomFrameǁpaintEvent__mutmut_28, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_29': xǁBlocksCustomFrameǁpaintEvent__mutmut_29, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_30': xǁBlocksCustomFrameǁpaintEvent__mutmut_30, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_31': xǁBlocksCustomFrameǁpaintEvent__mutmut_31, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_32': xǁBlocksCustomFrameǁpaintEvent__mutmut_32, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_33': xǁBlocksCustomFrameǁpaintEvent__mutmut_33, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_34': xǁBlocksCustomFrameǁpaintEvent__mutmut_34, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_35': xǁBlocksCustomFrameǁpaintEvent__mutmut_35, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_36': xǁBlocksCustomFrameǁpaintEvent__mutmut_36, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_37': xǁBlocksCustomFrameǁpaintEvent__mutmut_37, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_38': xǁBlocksCustomFrameǁpaintEvent__mutmut_38, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_39': xǁBlocksCustomFrameǁpaintEvent__mutmut_39, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_40': xǁBlocksCustomFrameǁpaintEvent__mutmut_40, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_41': xǁBlocksCustomFrameǁpaintEvent__mutmut_41, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_42': xǁBlocksCustomFrameǁpaintEvent__mutmut_42, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_43': xǁBlocksCustomFrameǁpaintEvent__mutmut_43, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_44': xǁBlocksCustomFrameǁpaintEvent__mutmut_44, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_45': xǁBlocksCustomFrameǁpaintEvent__mutmut_45, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_46': xǁBlocksCustomFrameǁpaintEvent__mutmut_46, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_47': xǁBlocksCustomFrameǁpaintEvent__mutmut_47, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_48': xǁBlocksCustomFrameǁpaintEvent__mutmut_48, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_49': xǁBlocksCustomFrameǁpaintEvent__mutmut_49, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_50': xǁBlocksCustomFrameǁpaintEvent__mutmut_50, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_51': xǁBlocksCustomFrameǁpaintEvent__mutmut_51, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_52': xǁBlocksCustomFrameǁpaintEvent__mutmut_52, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_53': xǁBlocksCustomFrameǁpaintEvent__mutmut_53, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_54': xǁBlocksCustomFrameǁpaintEvent__mutmut_54, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_55': xǁBlocksCustomFrameǁpaintEvent__mutmut_55, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_56': xǁBlocksCustomFrameǁpaintEvent__mutmut_56, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_57': xǁBlocksCustomFrameǁpaintEvent__mutmut_57, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_58': xǁBlocksCustomFrameǁpaintEvent__mutmut_58, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_59': xǁBlocksCustomFrameǁpaintEvent__mutmut_59, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_60': xǁBlocksCustomFrameǁpaintEvent__mutmut_60, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_61': xǁBlocksCustomFrameǁpaintEvent__mutmut_61, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_62': xǁBlocksCustomFrameǁpaintEvent__mutmut_62, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_63': xǁBlocksCustomFrameǁpaintEvent__mutmut_63, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_64': xǁBlocksCustomFrameǁpaintEvent__mutmut_64, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_65': xǁBlocksCustomFrameǁpaintEvent__mutmut_65, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_66': xǁBlocksCustomFrameǁpaintEvent__mutmut_66, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_67': xǁBlocksCustomFrameǁpaintEvent__mutmut_67, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_68': xǁBlocksCustomFrameǁpaintEvent__mutmut_68, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_69': xǁBlocksCustomFrameǁpaintEvent__mutmut_69, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_70': xǁBlocksCustomFrameǁpaintEvent__mutmut_70, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_71': xǁBlocksCustomFrameǁpaintEvent__mutmut_71, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_72': xǁBlocksCustomFrameǁpaintEvent__mutmut_72, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_73': xǁBlocksCustomFrameǁpaintEvent__mutmut_73, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_74': xǁBlocksCustomFrameǁpaintEvent__mutmut_74, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_75': xǁBlocksCustomFrameǁpaintEvent__mutmut_75, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_76': xǁBlocksCustomFrameǁpaintEvent__mutmut_76, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_77': xǁBlocksCustomFrameǁpaintEvent__mutmut_77, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_78': xǁBlocksCustomFrameǁpaintEvent__mutmut_78, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_79': xǁBlocksCustomFrameǁpaintEvent__mutmut_79, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_80': xǁBlocksCustomFrameǁpaintEvent__mutmut_80, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_81': xǁBlocksCustomFrameǁpaintEvent__mutmut_81, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_82': xǁBlocksCustomFrameǁpaintEvent__mutmut_82, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_83': xǁBlocksCustomFrameǁpaintEvent__mutmut_83, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_84': xǁBlocksCustomFrameǁpaintEvent__mutmut_84, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_85': xǁBlocksCustomFrameǁpaintEvent__mutmut_85, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_86': xǁBlocksCustomFrameǁpaintEvent__mutmut_86, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_87': xǁBlocksCustomFrameǁpaintEvent__mutmut_87, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_88': xǁBlocksCustomFrameǁpaintEvent__mutmut_88, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_89': xǁBlocksCustomFrameǁpaintEvent__mutmut_89, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_90': xǁBlocksCustomFrameǁpaintEvent__mutmut_90, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_91': xǁBlocksCustomFrameǁpaintEvent__mutmut_91, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_92': xǁBlocksCustomFrameǁpaintEvent__mutmut_92, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_93': xǁBlocksCustomFrameǁpaintEvent__mutmut_93, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_94': xǁBlocksCustomFrameǁpaintEvent__mutmut_94, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_95': xǁBlocksCustomFrameǁpaintEvent__mutmut_95, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_96': xǁBlocksCustomFrameǁpaintEvent__mutmut_96, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_97': xǁBlocksCustomFrameǁpaintEvent__mutmut_97, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_98': xǁBlocksCustomFrameǁpaintEvent__mutmut_98, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_99': xǁBlocksCustomFrameǁpaintEvent__mutmut_99, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_100': xǁBlocksCustomFrameǁpaintEvent__mutmut_100, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_101': xǁBlocksCustomFrameǁpaintEvent__mutmut_101, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_102': xǁBlocksCustomFrameǁpaintEvent__mutmut_102, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_103': xǁBlocksCustomFrameǁpaintEvent__mutmut_103, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_104': xǁBlocksCustomFrameǁpaintEvent__mutmut_104, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_105': xǁBlocksCustomFrameǁpaintEvent__mutmut_105, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_106': xǁBlocksCustomFrameǁpaintEvent__mutmut_106, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_107': xǁBlocksCustomFrameǁpaintEvent__mutmut_107, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_108': xǁBlocksCustomFrameǁpaintEvent__mutmut_108, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_109': xǁBlocksCustomFrameǁpaintEvent__mutmut_109, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_110': xǁBlocksCustomFrameǁpaintEvent__mutmut_110, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_111': xǁBlocksCustomFrameǁpaintEvent__mutmut_111, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_112': xǁBlocksCustomFrameǁpaintEvent__mutmut_112, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_113': xǁBlocksCustomFrameǁpaintEvent__mutmut_113, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_114': xǁBlocksCustomFrameǁpaintEvent__mutmut_114, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_115': xǁBlocksCustomFrameǁpaintEvent__mutmut_115, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_116': xǁBlocksCustomFrameǁpaintEvent__mutmut_116, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_117': xǁBlocksCustomFrameǁpaintEvent__mutmut_117, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_118': xǁBlocksCustomFrameǁpaintEvent__mutmut_118, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_119': xǁBlocksCustomFrameǁpaintEvent__mutmut_119, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_120': xǁBlocksCustomFrameǁpaintEvent__mutmut_120, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_121': xǁBlocksCustomFrameǁpaintEvent__mutmut_121, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_122': xǁBlocksCustomFrameǁpaintEvent__mutmut_122, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_123': xǁBlocksCustomFrameǁpaintEvent__mutmut_123, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_124': xǁBlocksCustomFrameǁpaintEvent__mutmut_124, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_125': xǁBlocksCustomFrameǁpaintEvent__mutmut_125, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_126': xǁBlocksCustomFrameǁpaintEvent__mutmut_126, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_127': xǁBlocksCustomFrameǁpaintEvent__mutmut_127, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_128': xǁBlocksCustomFrameǁpaintEvent__mutmut_128, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_129': xǁBlocksCustomFrameǁpaintEvent__mutmut_129, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_130': xǁBlocksCustomFrameǁpaintEvent__mutmut_130, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_131': xǁBlocksCustomFrameǁpaintEvent__mutmut_131, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_132': xǁBlocksCustomFrameǁpaintEvent__mutmut_132, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_133': xǁBlocksCustomFrameǁpaintEvent__mutmut_133, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_134': xǁBlocksCustomFrameǁpaintEvent__mutmut_134, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_135': xǁBlocksCustomFrameǁpaintEvent__mutmut_135, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_136': xǁBlocksCustomFrameǁpaintEvent__mutmut_136, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_137': xǁBlocksCustomFrameǁpaintEvent__mutmut_137, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_138': xǁBlocksCustomFrameǁpaintEvent__mutmut_138, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_139': xǁBlocksCustomFrameǁpaintEvent__mutmut_139, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_140': xǁBlocksCustomFrameǁpaintEvent__mutmut_140, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_141': xǁBlocksCustomFrameǁpaintEvent__mutmut_141, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_142': xǁBlocksCustomFrameǁpaintEvent__mutmut_142, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_143': xǁBlocksCustomFrameǁpaintEvent__mutmut_143, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_144': xǁBlocksCustomFrameǁpaintEvent__mutmut_144, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_145': xǁBlocksCustomFrameǁpaintEvent__mutmut_145, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_146': xǁBlocksCustomFrameǁpaintEvent__mutmut_146, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_147': xǁBlocksCustomFrameǁpaintEvent__mutmut_147, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_148': xǁBlocksCustomFrameǁpaintEvent__mutmut_148, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_149': xǁBlocksCustomFrameǁpaintEvent__mutmut_149, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_150': xǁBlocksCustomFrameǁpaintEvent__mutmut_150, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_151': xǁBlocksCustomFrameǁpaintEvent__mutmut_151, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_152': xǁBlocksCustomFrameǁpaintEvent__mutmut_152, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_153': xǁBlocksCustomFrameǁpaintEvent__mutmut_153, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_154': xǁBlocksCustomFrameǁpaintEvent__mutmut_154, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_155': xǁBlocksCustomFrameǁpaintEvent__mutmut_155, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_156': xǁBlocksCustomFrameǁpaintEvent__mutmut_156, 
        'xǁBlocksCustomFrameǁpaintEvent__mutmut_157': xǁBlocksCustomFrameǁpaintEvent__mutmut_157
    }
    xǁBlocksCustomFrameǁpaintEvent__mutmut_orig.__name__ = 'xǁBlocksCustomFrameǁpaintEvent'
