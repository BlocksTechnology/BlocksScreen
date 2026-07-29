import numpy as np
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


class CustomScrollBar(QtWidgets.QScrollBar):
    def __init__(self, parent=None):
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomScrollBarǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁCustomScrollBarǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁCustomScrollBarǁ__init____mutmut_orig(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(40)
    def xǁCustomScrollBarǁ__init____mutmut_1(self, parent=None):
        super().__init__(None)
        self.setFixedWidth(40)
    def xǁCustomScrollBarǁ__init____mutmut_2(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(None)
    def xǁCustomScrollBarǁ__init____mutmut_3(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(41)
    
    xǁCustomScrollBarǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomScrollBarǁ__init____mutmut_1': xǁCustomScrollBarǁ__init____mutmut_1, 
        'xǁCustomScrollBarǁ__init____mutmut_2': xǁCustomScrollBarǁ__init____mutmut_2, 
        'xǁCustomScrollBarǁ__init____mutmut_3': xǁCustomScrollBarǁ__init____mutmut_3
    }
    xǁCustomScrollBarǁ__init____mutmut_orig.__name__ = 'xǁCustomScrollBarǁ__init__'

    def paintEvent(self, event):
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomScrollBarǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁCustomScrollBarǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁCustomScrollBarǁpaintEvent__mutmut_orig(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_1(self, event):
        """Re-implemented method, paint widget"""
        painter = None
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_2(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(None)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_3(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_4(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, None)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_5(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_6(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, )
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_7(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, False)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_8(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(None, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_9(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, None)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_10(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_11(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, )
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_12(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, False)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_13(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(None, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_14(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, None)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_15(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_16(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, )

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_17(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, False)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_18(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = None
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_19(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(None, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_20(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, None, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_21(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, None, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_22(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, None)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_23(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_24(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_25(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_26(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, )
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_27(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(1, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_28(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 1, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_29(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, +35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_30(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -36, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_31(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 1)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_32(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = None
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_33(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = None
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_34(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = None

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_35(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = None

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_36(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 6

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_37(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val != min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_38(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = None

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_39(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int(None)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_40(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) / 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_41(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() * max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_42(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 101)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_43(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = None

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_44(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 / max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_45(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) * 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_46(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp(None, [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_47(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), None, [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_48(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], None) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_49(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp([15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_50(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_51(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], ) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_52(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [16, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_53(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 86], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_54(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [1, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_55(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 101]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_56(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 101 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_57(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = None
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_58(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            None
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_59(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) - 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_60(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step * (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_61(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() / page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_62(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val - page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_63(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val + min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_64(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 41
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_65(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = None

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_66(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            None
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_67(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val) * (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_68(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length) / (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_69(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() + base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_70(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val + min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_71(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val + min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_72(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = None

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_73(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            None,
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_74(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            None,
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_75(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            None,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_76(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            None,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_77(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_78(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_79(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_80(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_81(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(None),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_82(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() - handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_83(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = None

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_84(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            None,
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_85(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            None,
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_86(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_87(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_88(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(None),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_89(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(None),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_90(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(None, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_91(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, None)  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_92(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_93(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, )  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_94(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_95(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(None, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_96(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, None, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_97(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, None, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_98(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, None))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_99(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_100(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_101(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_102(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, ))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_103(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(165, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_104(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 165, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_105(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 165, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_106(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 101))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_107(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(None, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_108(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, None)  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_109(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_110(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, )  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_111(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(1.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_112(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(None, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_113(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, None, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_114(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, None, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_115(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, None))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_116(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_117(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_118(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_119(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, ))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_120(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(165, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_121(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 165, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_122(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 165, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_123(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 165))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_124(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(None, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_125(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, None)  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_126(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_127(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, )  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_128(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(2.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_129(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(None, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_130(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, None, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_131(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, None, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_132(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, None))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_133(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_134(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_135(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_136(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, ))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_137(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(165, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_138(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 165, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_139(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 165, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_140(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 101))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_141(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(None)
        painter.drawRoundedRect(handle_rect, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_142(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(None, 1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_143(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, None, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_144(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, None)

    def xǁCustomScrollBarǁpaintEvent__mutmut_145(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(1, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_146(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_147(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, )

    def xǁCustomScrollBarǁpaintEvent__mutmut_148(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 2, 1)

    def xǁCustomScrollBarǁpaintEvent__mutmut_149(self, event):
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        groove = self.rect().adjusted(0, 0, -35, 0)
        min_val, max_val = self.minimum(), self.maximum()
        page_step = self.pageStep()
        val = self.value()

        handle_width = 5

        if max_val == min_val:
            return

        handle_percentage = int((self.value() / max_val) * 100)

        val = np.interp((handle_percentage), [15, 85], [0, 100]) / 100 * max_val

        base_handle_length = int(
            (groove.height() * page_step / (max_val - min_val + page_step)) + 40
        )
        handle_pos = int(
            (groove.height() - base_handle_length)
            * (val - min_val)
            / (max_val - min_val)
        )

        handle_rect = QtCore.QRect(
            groove.x(),
            int(groove.y() + handle_pos),
            handle_width,
            base_handle_length,
        )

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(handle_rect.topLeft()),
            QtCore.QPointF(handle_rect.bottomLeft()),
        )

        gradient.setColorAt(0.0, QtGui.QColor(164, 164, 164, 100))  # Top
        gradient.setColorAt(0.5, QtGui.QColor(164, 164, 164, 164))  # Center
        gradient.setColorAt(1.0, QtGui.QColor(164, 164, 164, 100))  # Bottom
        painter.setBrush(gradient)
        painter.drawRoundedRect(handle_rect, 1, 2)
    
    xǁCustomScrollBarǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomScrollBarǁpaintEvent__mutmut_1': xǁCustomScrollBarǁpaintEvent__mutmut_1, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_2': xǁCustomScrollBarǁpaintEvent__mutmut_2, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_3': xǁCustomScrollBarǁpaintEvent__mutmut_3, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_4': xǁCustomScrollBarǁpaintEvent__mutmut_4, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_5': xǁCustomScrollBarǁpaintEvent__mutmut_5, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_6': xǁCustomScrollBarǁpaintEvent__mutmut_6, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_7': xǁCustomScrollBarǁpaintEvent__mutmut_7, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_8': xǁCustomScrollBarǁpaintEvent__mutmut_8, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_9': xǁCustomScrollBarǁpaintEvent__mutmut_9, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_10': xǁCustomScrollBarǁpaintEvent__mutmut_10, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_11': xǁCustomScrollBarǁpaintEvent__mutmut_11, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_12': xǁCustomScrollBarǁpaintEvent__mutmut_12, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_13': xǁCustomScrollBarǁpaintEvent__mutmut_13, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_14': xǁCustomScrollBarǁpaintEvent__mutmut_14, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_15': xǁCustomScrollBarǁpaintEvent__mutmut_15, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_16': xǁCustomScrollBarǁpaintEvent__mutmut_16, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_17': xǁCustomScrollBarǁpaintEvent__mutmut_17, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_18': xǁCustomScrollBarǁpaintEvent__mutmut_18, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_19': xǁCustomScrollBarǁpaintEvent__mutmut_19, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_20': xǁCustomScrollBarǁpaintEvent__mutmut_20, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_21': xǁCustomScrollBarǁpaintEvent__mutmut_21, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_22': xǁCustomScrollBarǁpaintEvent__mutmut_22, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_23': xǁCustomScrollBarǁpaintEvent__mutmut_23, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_24': xǁCustomScrollBarǁpaintEvent__mutmut_24, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_25': xǁCustomScrollBarǁpaintEvent__mutmut_25, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_26': xǁCustomScrollBarǁpaintEvent__mutmut_26, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_27': xǁCustomScrollBarǁpaintEvent__mutmut_27, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_28': xǁCustomScrollBarǁpaintEvent__mutmut_28, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_29': xǁCustomScrollBarǁpaintEvent__mutmut_29, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_30': xǁCustomScrollBarǁpaintEvent__mutmut_30, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_31': xǁCustomScrollBarǁpaintEvent__mutmut_31, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_32': xǁCustomScrollBarǁpaintEvent__mutmut_32, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_33': xǁCustomScrollBarǁpaintEvent__mutmut_33, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_34': xǁCustomScrollBarǁpaintEvent__mutmut_34, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_35': xǁCustomScrollBarǁpaintEvent__mutmut_35, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_36': xǁCustomScrollBarǁpaintEvent__mutmut_36, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_37': xǁCustomScrollBarǁpaintEvent__mutmut_37, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_38': xǁCustomScrollBarǁpaintEvent__mutmut_38, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_39': xǁCustomScrollBarǁpaintEvent__mutmut_39, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_40': xǁCustomScrollBarǁpaintEvent__mutmut_40, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_41': xǁCustomScrollBarǁpaintEvent__mutmut_41, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_42': xǁCustomScrollBarǁpaintEvent__mutmut_42, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_43': xǁCustomScrollBarǁpaintEvent__mutmut_43, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_44': xǁCustomScrollBarǁpaintEvent__mutmut_44, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_45': xǁCustomScrollBarǁpaintEvent__mutmut_45, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_46': xǁCustomScrollBarǁpaintEvent__mutmut_46, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_47': xǁCustomScrollBarǁpaintEvent__mutmut_47, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_48': xǁCustomScrollBarǁpaintEvent__mutmut_48, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_49': xǁCustomScrollBarǁpaintEvent__mutmut_49, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_50': xǁCustomScrollBarǁpaintEvent__mutmut_50, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_51': xǁCustomScrollBarǁpaintEvent__mutmut_51, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_52': xǁCustomScrollBarǁpaintEvent__mutmut_52, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_53': xǁCustomScrollBarǁpaintEvent__mutmut_53, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_54': xǁCustomScrollBarǁpaintEvent__mutmut_54, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_55': xǁCustomScrollBarǁpaintEvent__mutmut_55, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_56': xǁCustomScrollBarǁpaintEvent__mutmut_56, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_57': xǁCustomScrollBarǁpaintEvent__mutmut_57, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_58': xǁCustomScrollBarǁpaintEvent__mutmut_58, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_59': xǁCustomScrollBarǁpaintEvent__mutmut_59, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_60': xǁCustomScrollBarǁpaintEvent__mutmut_60, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_61': xǁCustomScrollBarǁpaintEvent__mutmut_61, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_62': xǁCustomScrollBarǁpaintEvent__mutmut_62, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_63': xǁCustomScrollBarǁpaintEvent__mutmut_63, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_64': xǁCustomScrollBarǁpaintEvent__mutmut_64, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_65': xǁCustomScrollBarǁpaintEvent__mutmut_65, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_66': xǁCustomScrollBarǁpaintEvent__mutmut_66, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_67': xǁCustomScrollBarǁpaintEvent__mutmut_67, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_68': xǁCustomScrollBarǁpaintEvent__mutmut_68, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_69': xǁCustomScrollBarǁpaintEvent__mutmut_69, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_70': xǁCustomScrollBarǁpaintEvent__mutmut_70, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_71': xǁCustomScrollBarǁpaintEvent__mutmut_71, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_72': xǁCustomScrollBarǁpaintEvent__mutmut_72, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_73': xǁCustomScrollBarǁpaintEvent__mutmut_73, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_74': xǁCustomScrollBarǁpaintEvent__mutmut_74, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_75': xǁCustomScrollBarǁpaintEvent__mutmut_75, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_76': xǁCustomScrollBarǁpaintEvent__mutmut_76, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_77': xǁCustomScrollBarǁpaintEvent__mutmut_77, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_78': xǁCustomScrollBarǁpaintEvent__mutmut_78, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_79': xǁCustomScrollBarǁpaintEvent__mutmut_79, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_80': xǁCustomScrollBarǁpaintEvent__mutmut_80, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_81': xǁCustomScrollBarǁpaintEvent__mutmut_81, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_82': xǁCustomScrollBarǁpaintEvent__mutmut_82, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_83': xǁCustomScrollBarǁpaintEvent__mutmut_83, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_84': xǁCustomScrollBarǁpaintEvent__mutmut_84, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_85': xǁCustomScrollBarǁpaintEvent__mutmut_85, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_86': xǁCustomScrollBarǁpaintEvent__mutmut_86, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_87': xǁCustomScrollBarǁpaintEvent__mutmut_87, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_88': xǁCustomScrollBarǁpaintEvent__mutmut_88, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_89': xǁCustomScrollBarǁpaintEvent__mutmut_89, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_90': xǁCustomScrollBarǁpaintEvent__mutmut_90, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_91': xǁCustomScrollBarǁpaintEvent__mutmut_91, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_92': xǁCustomScrollBarǁpaintEvent__mutmut_92, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_93': xǁCustomScrollBarǁpaintEvent__mutmut_93, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_94': xǁCustomScrollBarǁpaintEvent__mutmut_94, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_95': xǁCustomScrollBarǁpaintEvent__mutmut_95, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_96': xǁCustomScrollBarǁpaintEvent__mutmut_96, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_97': xǁCustomScrollBarǁpaintEvent__mutmut_97, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_98': xǁCustomScrollBarǁpaintEvent__mutmut_98, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_99': xǁCustomScrollBarǁpaintEvent__mutmut_99, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_100': xǁCustomScrollBarǁpaintEvent__mutmut_100, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_101': xǁCustomScrollBarǁpaintEvent__mutmut_101, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_102': xǁCustomScrollBarǁpaintEvent__mutmut_102, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_103': xǁCustomScrollBarǁpaintEvent__mutmut_103, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_104': xǁCustomScrollBarǁpaintEvent__mutmut_104, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_105': xǁCustomScrollBarǁpaintEvent__mutmut_105, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_106': xǁCustomScrollBarǁpaintEvent__mutmut_106, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_107': xǁCustomScrollBarǁpaintEvent__mutmut_107, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_108': xǁCustomScrollBarǁpaintEvent__mutmut_108, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_109': xǁCustomScrollBarǁpaintEvent__mutmut_109, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_110': xǁCustomScrollBarǁpaintEvent__mutmut_110, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_111': xǁCustomScrollBarǁpaintEvent__mutmut_111, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_112': xǁCustomScrollBarǁpaintEvent__mutmut_112, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_113': xǁCustomScrollBarǁpaintEvent__mutmut_113, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_114': xǁCustomScrollBarǁpaintEvent__mutmut_114, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_115': xǁCustomScrollBarǁpaintEvent__mutmut_115, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_116': xǁCustomScrollBarǁpaintEvent__mutmut_116, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_117': xǁCustomScrollBarǁpaintEvent__mutmut_117, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_118': xǁCustomScrollBarǁpaintEvent__mutmut_118, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_119': xǁCustomScrollBarǁpaintEvent__mutmut_119, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_120': xǁCustomScrollBarǁpaintEvent__mutmut_120, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_121': xǁCustomScrollBarǁpaintEvent__mutmut_121, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_122': xǁCustomScrollBarǁpaintEvent__mutmut_122, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_123': xǁCustomScrollBarǁpaintEvent__mutmut_123, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_124': xǁCustomScrollBarǁpaintEvent__mutmut_124, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_125': xǁCustomScrollBarǁpaintEvent__mutmut_125, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_126': xǁCustomScrollBarǁpaintEvent__mutmut_126, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_127': xǁCustomScrollBarǁpaintEvent__mutmut_127, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_128': xǁCustomScrollBarǁpaintEvent__mutmut_128, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_129': xǁCustomScrollBarǁpaintEvent__mutmut_129, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_130': xǁCustomScrollBarǁpaintEvent__mutmut_130, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_131': xǁCustomScrollBarǁpaintEvent__mutmut_131, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_132': xǁCustomScrollBarǁpaintEvent__mutmut_132, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_133': xǁCustomScrollBarǁpaintEvent__mutmut_133, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_134': xǁCustomScrollBarǁpaintEvent__mutmut_134, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_135': xǁCustomScrollBarǁpaintEvent__mutmut_135, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_136': xǁCustomScrollBarǁpaintEvent__mutmut_136, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_137': xǁCustomScrollBarǁpaintEvent__mutmut_137, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_138': xǁCustomScrollBarǁpaintEvent__mutmut_138, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_139': xǁCustomScrollBarǁpaintEvent__mutmut_139, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_140': xǁCustomScrollBarǁpaintEvent__mutmut_140, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_141': xǁCustomScrollBarǁpaintEvent__mutmut_141, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_142': xǁCustomScrollBarǁpaintEvent__mutmut_142, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_143': xǁCustomScrollBarǁpaintEvent__mutmut_143, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_144': xǁCustomScrollBarǁpaintEvent__mutmut_144, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_145': xǁCustomScrollBarǁpaintEvent__mutmut_145, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_146': xǁCustomScrollBarǁpaintEvent__mutmut_146, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_147': xǁCustomScrollBarǁpaintEvent__mutmut_147, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_148': xǁCustomScrollBarǁpaintEvent__mutmut_148, 
        'xǁCustomScrollBarǁpaintEvent__mutmut_149': xǁCustomScrollBarǁpaintEvent__mutmut_149
    }
    xǁCustomScrollBarǁpaintEvent__mutmut_orig.__name__ = 'xǁCustomScrollBarǁpaintEvent'
