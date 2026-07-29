import typing
from PyQt6 import QtWidgets, QtGui, QtCore
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


class CustomProgressBar(QtWidgets.QProgressBar):
    """Custom circular progress bar for tracking print jobs

    Args:
        QtWidgets (QtWidget): Parent widget

    Raises:
        ValueError: Thrown when setting progress is not between 0.0 and 1.0
        ValueError: Thrown when setting bar color is not between 0 and 255.

    """

    thumbnail_clicked: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        name="thumbnail-clicked"
    )

    def __init__(self, parent=None):
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁ__init____mutmut_orig(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_1(self, parent=None):
        super().__init__(None)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_2(self, parent=None):
        super().__init__(parent)
        self.progress_value = None
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_3(self, parent=None):
        super().__init__(parent)
        self.progress_value = 1
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_4(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = None
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_5(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 21
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_6(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = None
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_7(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 51
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_8(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = None
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_9(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = None
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_10(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = None
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_11(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = False
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_12(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = None
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_13(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(None, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_14(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, None, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_15(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, None)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_16(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_17(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_18(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, )
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_19(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(224, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_20(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 224, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_21(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 224)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_22(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(None, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_23(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, None)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_24(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_25(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, )
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_26(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(101, 100)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_27(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 101)
        self._inner_rect: QtCore.QRectF = QtCore.QRectF()

    def xǁCustomProgressBarǁ__init____mutmut_28(self, parent=None):
        super().__init__(parent)
        self.progress_value = 0
        self._pen_width = 20
        self._padding = 50
        self._pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_cached: QtGui.QPixmap = QtGui.QPixmap()
        self._pixmap_dirty: bool = True
        self._bar_color = QtGui.QColor(223, 223, 223)
        self.setMinimumSize(100, 100)
        self._inner_rect: QtCore.QRectF = None
    
    xǁCustomProgressBarǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁ__init____mutmut_1': xǁCustomProgressBarǁ__init____mutmut_1, 
        'xǁCustomProgressBarǁ__init____mutmut_2': xǁCustomProgressBarǁ__init____mutmut_2, 
        'xǁCustomProgressBarǁ__init____mutmut_3': xǁCustomProgressBarǁ__init____mutmut_3, 
        'xǁCustomProgressBarǁ__init____mutmut_4': xǁCustomProgressBarǁ__init____mutmut_4, 
        'xǁCustomProgressBarǁ__init____mutmut_5': xǁCustomProgressBarǁ__init____mutmut_5, 
        'xǁCustomProgressBarǁ__init____mutmut_6': xǁCustomProgressBarǁ__init____mutmut_6, 
        'xǁCustomProgressBarǁ__init____mutmut_7': xǁCustomProgressBarǁ__init____mutmut_7, 
        'xǁCustomProgressBarǁ__init____mutmut_8': xǁCustomProgressBarǁ__init____mutmut_8, 
        'xǁCustomProgressBarǁ__init____mutmut_9': xǁCustomProgressBarǁ__init____mutmut_9, 
        'xǁCustomProgressBarǁ__init____mutmut_10': xǁCustomProgressBarǁ__init____mutmut_10, 
        'xǁCustomProgressBarǁ__init____mutmut_11': xǁCustomProgressBarǁ__init____mutmut_11, 
        'xǁCustomProgressBarǁ__init____mutmut_12': xǁCustomProgressBarǁ__init____mutmut_12, 
        'xǁCustomProgressBarǁ__init____mutmut_13': xǁCustomProgressBarǁ__init____mutmut_13, 
        'xǁCustomProgressBarǁ__init____mutmut_14': xǁCustomProgressBarǁ__init____mutmut_14, 
        'xǁCustomProgressBarǁ__init____mutmut_15': xǁCustomProgressBarǁ__init____mutmut_15, 
        'xǁCustomProgressBarǁ__init____mutmut_16': xǁCustomProgressBarǁ__init____mutmut_16, 
        'xǁCustomProgressBarǁ__init____mutmut_17': xǁCustomProgressBarǁ__init____mutmut_17, 
        'xǁCustomProgressBarǁ__init____mutmut_18': xǁCustomProgressBarǁ__init____mutmut_18, 
        'xǁCustomProgressBarǁ__init____mutmut_19': xǁCustomProgressBarǁ__init____mutmut_19, 
        'xǁCustomProgressBarǁ__init____mutmut_20': xǁCustomProgressBarǁ__init____mutmut_20, 
        'xǁCustomProgressBarǁ__init____mutmut_21': xǁCustomProgressBarǁ__init____mutmut_21, 
        'xǁCustomProgressBarǁ__init____mutmut_22': xǁCustomProgressBarǁ__init____mutmut_22, 
        'xǁCustomProgressBarǁ__init____mutmut_23': xǁCustomProgressBarǁ__init____mutmut_23, 
        'xǁCustomProgressBarǁ__init____mutmut_24': xǁCustomProgressBarǁ__init____mutmut_24, 
        'xǁCustomProgressBarǁ__init____mutmut_25': xǁCustomProgressBarǁ__init____mutmut_25, 
        'xǁCustomProgressBarǁ__init____mutmut_26': xǁCustomProgressBarǁ__init____mutmut_26, 
        'xǁCustomProgressBarǁ__init____mutmut_27': xǁCustomProgressBarǁ__init____mutmut_27, 
        'xǁCustomProgressBarǁ__init____mutmut_28': xǁCustomProgressBarǁ__init____mutmut_28
    }
    xǁCustomProgressBarǁ__init____mutmut_orig.__name__ = 'xǁCustomProgressBarǁ__init__'

    def set_padding(self, value) -> None:
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁset_padding__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁset_padding__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁset_padding__mutmut_orig(self, value) -> None:
        """Set widget padding"""
        self._padding = value
        self.update()

    def xǁCustomProgressBarǁset_padding__mutmut_1(self, value) -> None:
        """Set widget padding"""
        self._padding = None
        self.update()
    
    xǁCustomProgressBarǁset_padding__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁset_padding__mutmut_1': xǁCustomProgressBarǁset_padding__mutmut_1
    }
    xǁCustomProgressBarǁset_padding__mutmut_orig.__name__ = 'xǁCustomProgressBarǁset_padding'

    def set_pen_width(self, value) -> None:
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁset_pen_width__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁset_pen_width__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁset_pen_width__mutmut_orig(self, value) -> None:
        """Set widget text pen width"""
        self._pen_width = value
        self.update()

    def xǁCustomProgressBarǁset_pen_width__mutmut_1(self, value) -> None:
        """Set widget text pen width"""
        self._pen_width = None
        self.update()
    
    xǁCustomProgressBarǁset_pen_width__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁset_pen_width__mutmut_1': xǁCustomProgressBarǁset_pen_width__mutmut_1
    }
    xǁCustomProgressBarǁset_pen_width__mutmut_orig.__name__ = 'xǁCustomProgressBarǁset_pen_width'

    def _scale_pixmap(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁ_scale_pixmap__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁ_scale_pixmap__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_orig(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_1(self) -> None:
        self._inner_rect = None
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_2(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = None

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_3(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            None,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_4(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            None,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_5(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            None,
        )

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_6(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_7(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

    def xǁCustomProgressBarǁ_scale_pixmap__mutmut_8(self) -> None:
        self._inner_rect = self._calculate_inner_geometry()
        self._pixmap_cached = self._pixmap.scaled(
            self._inner_rect.size().toSize(),
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            )
    
    xǁCustomProgressBarǁ_scale_pixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁ_scale_pixmap__mutmut_1': xǁCustomProgressBarǁ_scale_pixmap__mutmut_1, 
        'xǁCustomProgressBarǁ_scale_pixmap__mutmut_2': xǁCustomProgressBarǁ_scale_pixmap__mutmut_2, 
        'xǁCustomProgressBarǁ_scale_pixmap__mutmut_3': xǁCustomProgressBarǁ_scale_pixmap__mutmut_3, 
        'xǁCustomProgressBarǁ_scale_pixmap__mutmut_4': xǁCustomProgressBarǁ_scale_pixmap__mutmut_4, 
        'xǁCustomProgressBarǁ_scale_pixmap__mutmut_5': xǁCustomProgressBarǁ_scale_pixmap__mutmut_5, 
        'xǁCustomProgressBarǁ_scale_pixmap__mutmut_6': xǁCustomProgressBarǁ_scale_pixmap__mutmut_6, 
        'xǁCustomProgressBarǁ_scale_pixmap__mutmut_7': xǁCustomProgressBarǁ_scale_pixmap__mutmut_7, 
        'xǁCustomProgressBarǁ_scale_pixmap__mutmut_8': xǁCustomProgressBarǁ_scale_pixmap__mutmut_8
    }
    xǁCustomProgressBarǁ_scale_pixmap__mutmut_orig.__name__ = 'xǁCustomProgressBarǁ_scale_pixmap'

    def set_inner_pixmap(self, pixmap: QtGui.QPixmap) -> None:
        args = [pixmap]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁset_inner_pixmap__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁset_inner_pixmap__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁset_inner_pixmap__mutmut_orig(self, pixmap: QtGui.QPixmap) -> None:
        """Set the inner icon pixmap on the progress bar
        circumference.
        """
        self._pixmap = pixmap
        self._scale_pixmap()

    def xǁCustomProgressBarǁset_inner_pixmap__mutmut_1(self, pixmap: QtGui.QPixmap) -> None:
        """Set the inner icon pixmap on the progress bar
        circumference.
        """
        self._pixmap = None
        self._scale_pixmap()
    
    xǁCustomProgressBarǁset_inner_pixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁset_inner_pixmap__mutmut_1': xǁCustomProgressBarǁset_inner_pixmap__mutmut_1
    }
    xǁCustomProgressBarǁset_inner_pixmap__mutmut_orig.__name__ = 'xǁCustomProgressBarǁset_inner_pixmap'

    def resizeEvent(self, a0) -> None:
        """Reimplemented method, handle widget resize Events

        Currently rescales the set pixmap so it has the optimal
        size.
        """
        self._scale_pixmap()
        self.update()

    def sizeHint(self) -> QtCore.QSize:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁsizeHint__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁsizeHint__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁsizeHint__mutmut_orig(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 100)

    def xǁCustomProgressBarǁsizeHint__mutmut_1(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = None
        return QtCore.QSize(100, 100)

    def xǁCustomProgressBarǁsizeHint__mutmut_2(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(None, 100)

    def xǁCustomProgressBarǁsizeHint__mutmut_3(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, None)

    def xǁCustomProgressBarǁsizeHint__mutmut_4(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100)

    def xǁCustomProgressBarǁsizeHint__mutmut_5(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, )

    def xǁCustomProgressBarǁsizeHint__mutmut_6(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(101, 100)

    def xǁCustomProgressBarǁsizeHint__mutmut_7(self) -> QtCore.QSize:
        """Re-implemented method, preferable widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 101)
    
    xǁCustomProgressBarǁsizeHint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁsizeHint__mutmut_1': xǁCustomProgressBarǁsizeHint__mutmut_1, 
        'xǁCustomProgressBarǁsizeHint__mutmut_2': xǁCustomProgressBarǁsizeHint__mutmut_2, 
        'xǁCustomProgressBarǁsizeHint__mutmut_3': xǁCustomProgressBarǁsizeHint__mutmut_3, 
        'xǁCustomProgressBarǁsizeHint__mutmut_4': xǁCustomProgressBarǁsizeHint__mutmut_4, 
        'xǁCustomProgressBarǁsizeHint__mutmut_5': xǁCustomProgressBarǁsizeHint__mutmut_5, 
        'xǁCustomProgressBarǁsizeHint__mutmut_6': xǁCustomProgressBarǁsizeHint__mutmut_6, 
        'xǁCustomProgressBarǁsizeHint__mutmut_7': xǁCustomProgressBarǁsizeHint__mutmut_7
    }
    xǁCustomProgressBarǁsizeHint__mutmut_orig.__name__ = 'xǁCustomProgressBarǁsizeHint'

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁmousePressEvent__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁmousePressEvent__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁmousePressEvent__mutmut_orig(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, check if thumbnail was clicked,
        filter clicks inside inner section of the widget,
        if a mouse event happens there we know that the thumbnail
        was pressed.
        """
        if self._inner_rect.contains(a0.pos().x(), a0.pos().y()):
            self.thumbnail_clicked.emit()
        return super().mousePressEvent(a0)

    def xǁCustomProgressBarǁmousePressEvent__mutmut_1(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, check if thumbnail was clicked,
        filter clicks inside inner section of the widget,
        if a mouse event happens there we know that the thumbnail
        was pressed.
        """
        if self._inner_rect.contains(None, a0.pos().y()):
            self.thumbnail_clicked.emit()
        return super().mousePressEvent(a0)

    def xǁCustomProgressBarǁmousePressEvent__mutmut_2(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, check if thumbnail was clicked,
        filter clicks inside inner section of the widget,
        if a mouse event happens there we know that the thumbnail
        was pressed.
        """
        if self._inner_rect.contains(a0.pos().x(), None):
            self.thumbnail_clicked.emit()
        return super().mousePressEvent(a0)

    def xǁCustomProgressBarǁmousePressEvent__mutmut_3(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, check if thumbnail was clicked,
        filter clicks inside inner section of the widget,
        if a mouse event happens there we know that the thumbnail
        was pressed.
        """
        if self._inner_rect.contains(a0.pos().y()):
            self.thumbnail_clicked.emit()
        return super().mousePressEvent(a0)

    def xǁCustomProgressBarǁmousePressEvent__mutmut_4(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, check if thumbnail was clicked,
        filter clicks inside inner section of the widget,
        if a mouse event happens there we know that the thumbnail
        was pressed.
        """
        if self._inner_rect.contains(a0.pos().x(), ):
            self.thumbnail_clicked.emit()
        return super().mousePressEvent(a0)

    def xǁCustomProgressBarǁmousePressEvent__mutmut_5(self, a0: QtGui.QMouseEvent) -> None:
        """Re-implemented method, check if thumbnail was clicked,
        filter clicks inside inner section of the widget,
        if a mouse event happens there we know that the thumbnail
        was pressed.
        """
        if self._inner_rect.contains(a0.pos().x(), a0.pos().y()):
            self.thumbnail_clicked.emit()
        return super().mousePressEvent(None)
    
    xǁCustomProgressBarǁmousePressEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁmousePressEvent__mutmut_1': xǁCustomProgressBarǁmousePressEvent__mutmut_1, 
        'xǁCustomProgressBarǁmousePressEvent__mutmut_2': xǁCustomProgressBarǁmousePressEvent__mutmut_2, 
        'xǁCustomProgressBarǁmousePressEvent__mutmut_3': xǁCustomProgressBarǁmousePressEvent__mutmut_3, 
        'xǁCustomProgressBarǁmousePressEvent__mutmut_4': xǁCustomProgressBarǁmousePressEvent__mutmut_4, 
        'xǁCustomProgressBarǁmousePressEvent__mutmut_5': xǁCustomProgressBarǁmousePressEvent__mutmut_5
    }
    xǁCustomProgressBarǁmousePressEvent__mutmut_orig.__name__ = 'xǁCustomProgressBarǁmousePressEvent'

    def minimumSizeHint(self) -> QtCore.QSize:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁminimumSizeHint__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁminimumSizeHint__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_orig(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 100)

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_1(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = None
        return QtCore.QSize(100, 100)

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_2(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(None, 100)

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_3(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, None)

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_4(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100)

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_5(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, )

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_6(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(101, 100)

    def xǁCustomProgressBarǁminimumSizeHint__mutmut_7(self) -> QtCore.QSize:
        """Re-implemented method, minimum widget size"""
        self._inner_rect = self._calculate_inner_geometry()
        return QtCore.QSize(100, 101)
    
    xǁCustomProgressBarǁminimumSizeHint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁminimumSizeHint__mutmut_1': xǁCustomProgressBarǁminimumSizeHint__mutmut_1, 
        'xǁCustomProgressBarǁminimumSizeHint__mutmut_2': xǁCustomProgressBarǁminimumSizeHint__mutmut_2, 
        'xǁCustomProgressBarǁminimumSizeHint__mutmut_3': xǁCustomProgressBarǁminimumSizeHint__mutmut_3, 
        'xǁCustomProgressBarǁminimumSizeHint__mutmut_4': xǁCustomProgressBarǁminimumSizeHint__mutmut_4, 
        'xǁCustomProgressBarǁminimumSizeHint__mutmut_5': xǁCustomProgressBarǁminimumSizeHint__mutmut_5, 
        'xǁCustomProgressBarǁminimumSizeHint__mutmut_6': xǁCustomProgressBarǁminimumSizeHint__mutmut_6, 
        'xǁCustomProgressBarǁminimumSizeHint__mutmut_7': xǁCustomProgressBarǁminimumSizeHint__mutmut_7
    }
    xǁCustomProgressBarǁminimumSizeHint__mutmut_orig.__name__ = 'xǁCustomProgressBarǁminimumSizeHint'

    def setValue(self, value: float) -> None:
        args = [value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁsetValue__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁsetValue__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁsetValue__mutmut_orig(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_1(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if (0 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_2(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (1 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_3(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 < value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_4(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value < 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_5(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 101):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_6(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError(None)
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_7(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("XXArgument `value` expected value between 0.0 and 1.0 XX")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_8(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_9(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("ARGUMENT `VALUE` EXPECTED VALUE BETWEEN 0.0 AND 1.0 ")
        value *= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_10(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value = 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_11(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value /= 100
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_12(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 101
        self.progress_value = value
        self.update()

    def xǁCustomProgressBarǁsetValue__mutmut_13(self, value: float) -> None:
        """Set progress value

        Args:
            value (float): Progress value between 0.0 and 1.0

        Raises:
            ValueError: If provided value in not between 0.0 and 1.0
        """
        if not (0 <= value <= 100):
            raise ValueError("Argument `value` expected value between 0.0 and 1.0 ")
        value *= 100
        self.progress_value = None
        self.update()
    
    xǁCustomProgressBarǁsetValue__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁsetValue__mutmut_1': xǁCustomProgressBarǁsetValue__mutmut_1, 
        'xǁCustomProgressBarǁsetValue__mutmut_2': xǁCustomProgressBarǁsetValue__mutmut_2, 
        'xǁCustomProgressBarǁsetValue__mutmut_3': xǁCustomProgressBarǁsetValue__mutmut_3, 
        'xǁCustomProgressBarǁsetValue__mutmut_4': xǁCustomProgressBarǁsetValue__mutmut_4, 
        'xǁCustomProgressBarǁsetValue__mutmut_5': xǁCustomProgressBarǁsetValue__mutmut_5, 
        'xǁCustomProgressBarǁsetValue__mutmut_6': xǁCustomProgressBarǁsetValue__mutmut_6, 
        'xǁCustomProgressBarǁsetValue__mutmut_7': xǁCustomProgressBarǁsetValue__mutmut_7, 
        'xǁCustomProgressBarǁsetValue__mutmut_8': xǁCustomProgressBarǁsetValue__mutmut_8, 
        'xǁCustomProgressBarǁsetValue__mutmut_9': xǁCustomProgressBarǁsetValue__mutmut_9, 
        'xǁCustomProgressBarǁsetValue__mutmut_10': xǁCustomProgressBarǁsetValue__mutmut_10, 
        'xǁCustomProgressBarǁsetValue__mutmut_11': xǁCustomProgressBarǁsetValue__mutmut_11, 
        'xǁCustomProgressBarǁsetValue__mutmut_12': xǁCustomProgressBarǁsetValue__mutmut_12, 
        'xǁCustomProgressBarǁsetValue__mutmut_13': xǁCustomProgressBarǁsetValue__mutmut_13
    }
    xǁCustomProgressBarǁsetValue__mutmut_orig.__name__ = 'xǁCustomProgressBarǁsetValue'

    def set_bar_color(self, red: int, green: int, blue: int) -> None:
        args = [red, green, blue]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁset_bar_color__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁset_bar_color__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁset_bar_color__mutmut_orig(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_1(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_2(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 or 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_3(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 or 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_4(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (1 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_5(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 < red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_6(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red < 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_7(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 256 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_8(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 1 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_9(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 < green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_10(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green < 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_11(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 256 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_12(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 1 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_13(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 < blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_14(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue < 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_15(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 256):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_16(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError(None)
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_17(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("XXColor values must be between 0 and 255.XX")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_18(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_19(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("COLOR VALUES MUST BE BETWEEN 0 AND 255.")
        self._bar_color = QtGui.QColor(red, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_20(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = None
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_21(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(None, green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_22(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, None, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_23(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, None)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_24(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(green, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_25(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, blue)
        self.update()

    def xǁCustomProgressBarǁset_bar_color__mutmut_26(self, red: int, green: int, blue: int) -> None:
        """Set widget progress bar color

        Args:
            red (int): red component value between 0 and 255
            green (int): green component value between 0 and 255
            blue (int): blue component value between 0 and 255

        Raises:
            ValueError: Raised if any provided argument value is not between 0 and 255
        """
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        self._bar_color = QtGui.QColor(red, green, )
        self.update()
    
    xǁCustomProgressBarǁset_bar_color__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁset_bar_color__mutmut_1': xǁCustomProgressBarǁset_bar_color__mutmut_1, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_2': xǁCustomProgressBarǁset_bar_color__mutmut_2, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_3': xǁCustomProgressBarǁset_bar_color__mutmut_3, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_4': xǁCustomProgressBarǁset_bar_color__mutmut_4, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_5': xǁCustomProgressBarǁset_bar_color__mutmut_5, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_6': xǁCustomProgressBarǁset_bar_color__mutmut_6, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_7': xǁCustomProgressBarǁset_bar_color__mutmut_7, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_8': xǁCustomProgressBarǁset_bar_color__mutmut_8, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_9': xǁCustomProgressBarǁset_bar_color__mutmut_9, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_10': xǁCustomProgressBarǁset_bar_color__mutmut_10, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_11': xǁCustomProgressBarǁset_bar_color__mutmut_11, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_12': xǁCustomProgressBarǁset_bar_color__mutmut_12, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_13': xǁCustomProgressBarǁset_bar_color__mutmut_13, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_14': xǁCustomProgressBarǁset_bar_color__mutmut_14, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_15': xǁCustomProgressBarǁset_bar_color__mutmut_15, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_16': xǁCustomProgressBarǁset_bar_color__mutmut_16, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_17': xǁCustomProgressBarǁset_bar_color__mutmut_17, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_18': xǁCustomProgressBarǁset_bar_color__mutmut_18, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_19': xǁCustomProgressBarǁset_bar_color__mutmut_19, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_20': xǁCustomProgressBarǁset_bar_color__mutmut_20, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_21': xǁCustomProgressBarǁset_bar_color__mutmut_21, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_22': xǁCustomProgressBarǁset_bar_color__mutmut_22, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_23': xǁCustomProgressBarǁset_bar_color__mutmut_23, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_24': xǁCustomProgressBarǁset_bar_color__mutmut_24, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_25': xǁCustomProgressBarǁset_bar_color__mutmut_25, 
        'xǁCustomProgressBarǁset_bar_color__mutmut_26': xǁCustomProgressBarǁset_bar_color__mutmut_26
    }
    xǁCustomProgressBarǁset_bar_color__mutmut_orig.__name__ = 'xǁCustomProgressBarǁset_bar_color'

    def _calculate_inner_geometry(self) -> QtCore.QRectF:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_orig(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_1(self) -> QtCore.QRectF:
        size = None
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_2(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) + (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_3(self) -> QtCore.QRectF:
        size = min(None, self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_4(self) -> QtCore.QRectF:
        size = min(self.width(), None) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_5(self) -> QtCore.QRectF:
        size = min(self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_6(self) -> QtCore.QRectF:
        size = min(self.width(), ) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_7(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding / 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_8(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 2.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_9(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = None
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_10(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_11(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() + size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_12(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 3
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_13(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = None
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_14(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) / 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_15(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() + size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_16(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 3
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_17(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            None,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_18(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            None,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_19(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            None,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_20(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            None,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_21(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_22(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_23(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_24(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_25(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x - self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_26(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width / 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_27(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 3,
            y + self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_28(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y - self._pen_width // 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_29(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width / 2,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_30(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 3,
            size - self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_31(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size + self._pen_width,
            size - self._pen_width,
        )

    def xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_32(self) -> QtCore.QRectF:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        return QtCore.QRectF(
            x + self._pen_width // 2,
            y + self._pen_width // 2,
            size - self._pen_width,
            size + self._pen_width,
        )
    
    xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_1': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_1, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_2': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_2, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_3': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_3, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_4': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_4, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_5': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_5, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_6': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_6, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_7': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_7, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_8': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_8, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_9': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_9, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_10': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_10, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_11': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_11, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_12': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_12, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_13': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_13, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_14': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_14, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_15': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_15, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_16': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_16, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_17': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_17, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_18': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_18, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_19': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_19, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_20': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_20, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_21': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_21, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_22': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_22, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_23': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_23, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_24': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_24, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_25': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_25, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_26': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_26, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_27': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_27, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_28': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_28, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_29': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_29, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_30': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_30, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_31': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_31, 
        'xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_32': xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_32
    }
    xǁCustomProgressBarǁ_calculate_inner_geometry__mutmut_orig.__name__ = 'xǁCustomProgressBarǁ_calculate_inner_geometry'

    def _draw_cached_pixmap(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        args = [painter, pixmap, inner_rect]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_orig(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_1(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = None
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_2(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = None
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_3(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = None
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_4(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) / 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_5(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() + scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_6(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 3.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_7(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = None
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_8(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) / 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_9(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() + scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_10(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 3.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_11(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = None
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_12(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            None,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_13(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            None,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_14(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            None,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_15(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            None,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_16(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_17(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_18(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_19(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_20(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() - adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_21(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() - adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_22(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(None, pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_23(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, None, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_24(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, None)

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_25(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(pixmap, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_26(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap.rect().toRectF())

    def xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_27(
        self, painter: QtGui.QPainter, pixmap: QtGui.QPixmap, inner_rect: QtCore.QRectF
    ) -> None:
        """Internal method draw already scaled pixmap on the widget inner section"""
        if pixmap.isNull():
            return
        scaled_width = pixmap.width()
        scaled_height = pixmap.height()
        adjusted_x = (inner_rect.width() - scaled_width) // 2.0
        adjusted_y = (inner_rect.height() - scaled_height) // 2.0
        adjusted_icon = QtCore.QRectF(
            inner_rect.x() + adjusted_x,
            inner_rect.y() + adjusted_y,
            scaled_width,
            scaled_height,
        )
        painter.drawPixmap(adjusted_icon, pixmap, )
    
    xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_1': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_1, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_2': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_2, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_3': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_3, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_4': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_4, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_5': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_5, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_6': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_6, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_7': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_7, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_8': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_8, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_9': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_9, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_10': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_10, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_11': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_11, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_12': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_12, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_13': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_13, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_14': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_14, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_15': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_15, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_16': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_16, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_17': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_17, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_18': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_18, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_19': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_19, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_20': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_20, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_21': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_21, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_22': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_22, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_23': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_23, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_24': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_24, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_25': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_25, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_26': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_26, 
        'xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_27': xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_27
    }
    xǁCustomProgressBarǁ_draw_cached_pixmap__mutmut_orig.__name__ = 'xǁCustomProgressBarǁ_draw_cached_pixmap'

    def _draw_circular_bar(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        args = [painter]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_orig(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_1(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = None
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_2(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) + (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_3(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(None, self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_4(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), None) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_5(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_6(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), ) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_7(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding / 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_8(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 2.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_9(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = None
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_10(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) * 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_11(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() + size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_12(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 3
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_13(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = None
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_14(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) * 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_15(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() + size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_16(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 3
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_17(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = None
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_18(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(None, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_19(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, None, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_20(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, None, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_21(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, None)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_22(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_23(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_24(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_25(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, )
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_26(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = None
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_27(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 / 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_28(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 237 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_29(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 17
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_30(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = None
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_31(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 / 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_32(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = +290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_33(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -291 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_34(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 17
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_35(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = None
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_36(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(None)
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_37(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(None, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_38(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, None, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_39(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, None))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_40(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_41(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_42(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, ))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_43(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(21, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_44(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 21, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_45(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 21))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_46(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(None)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_47(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(None)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_48(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(None)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_49(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(None, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_50(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, None, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_51(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, None)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_52(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_53(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_54(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, )
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_55(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_56(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = None
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_57(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(None, -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_58(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), None)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_59(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(-90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_60(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), )
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_61(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), +90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_62(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -91)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_63(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(None, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_64(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, None)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_65(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_66(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, )
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_67(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(1.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_68(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(None, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_69(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, None)
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_70(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_71(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, )
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_72(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(2.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_73(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(None, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_74(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, None, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_75(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, None))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_76(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_77(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_78(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, ))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_79(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(101, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_80(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 101, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_81(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 101))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_82(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = None
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_83(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(None)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_84(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(None)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_85(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(None)
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_86(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(None))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_87(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(None)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_88(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = None
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_89(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(None)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_90(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value * 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_91(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span / self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_92(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 101)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_93(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(None, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_94(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, None, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_95(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, None)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_96(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_97(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_98(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, )
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_99(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = None
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_100(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(None)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_101(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(None)
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_102(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(None))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_103(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(None, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_104(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, None, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_105(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, None)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_106(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_107(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_108(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, )))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_109(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(1, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_110(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 1, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_111(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 1)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_112(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = None
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_113(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(None)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_114(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(17)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_115(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = None
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_116(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(None)
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_117(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(None, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_118(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, None, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_119(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, None))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_120(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_121(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_122(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, ))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_123(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(256, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_124(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 256, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_125(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 256))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_126(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(None)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_127(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(None)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_128(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = None
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_129(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = None
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_130(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = None
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_131(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            None, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_132(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, None, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_133(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, None, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_134(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, None
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_135(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_136(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_137(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_138(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_139(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x + 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_140(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 31, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_141(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 + 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_142(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y - arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_143(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() * 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_144(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 3 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_145(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 26, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_146(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 61, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_147(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 41
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_148(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(None, QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_149(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, None, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_150(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, None)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_151(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(QtCore.Qt.AlignmentFlag.AlignCenter, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_152(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, progress_text)

    def xǁCustomProgressBarǁ_draw_circular_bar__mutmut_153(
        self,
        painter: QtGui.QPainter,
    ) -> None:
        size = min(self.width(), self.height()) - (self._padding * 1.3)
        x = (self.width() - size) / 2
        y = (self.height() - size) / 2
        arc_rect = QtCore.QRectF(x, y, size, size)
        arc_start = 236 * 16
        arc_span = -290 * 16
        bg_pen = QtGui.QPen(QtGui.QColor(20, 20, 20))
        bg_pen.setWidth(self._pen_width)
        bg_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(arc_rect, arc_start, arc_span)
        if self.progress_value is not None:
            gradient = QtGui.QConicalGradient(arc_rect.center(), -90)
            gradient.setColorAt(0.0, self._bar_color)
            gradient.setColorAt(1.0, QtGui.QColor(100, 100, 100))
            progress_pen = QtGui.QPen()
            progress_pen.setWidth(self._pen_width)
            progress_pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
            progress_pen.setBrush(QtGui.QBrush(gradient))
            painter.setPen(progress_pen)
            # scale only over arc span
            progress_span = int(arc_span * self.progress_value / 100)
            painter.drawArc(arc_rect, arc_start, progress_span)
        progress_text = f"{int(self.progress_value)}%"
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        font = painter.font()
        font.setPointSize(16)
        bg_pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(bg_pen)
        painter.setFont(font)
        text_x = arc_rect.center().x()
        text_y = arc_rect.center().y()
        text_rect = QtCore.QRectF(
            text_x - 30, text_y + arc_rect.height() / 2 - 25, 60, 40
        )
        painter.drawText(text_rect, QtCore.Qt.AlignmentFlag.AlignCenter, )
    
    xǁCustomProgressBarǁ_draw_circular_bar__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_1': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_1, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_2': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_2, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_3': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_3, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_4': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_4, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_5': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_5, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_6': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_6, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_7': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_7, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_8': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_8, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_9': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_9, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_10': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_10, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_11': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_11, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_12': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_12, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_13': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_13, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_14': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_14, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_15': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_15, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_16': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_16, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_17': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_17, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_18': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_18, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_19': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_19, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_20': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_20, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_21': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_21, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_22': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_22, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_23': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_23, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_24': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_24, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_25': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_25, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_26': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_26, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_27': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_27, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_28': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_28, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_29': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_29, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_30': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_30, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_31': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_31, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_32': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_32, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_33': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_33, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_34': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_34, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_35': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_35, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_36': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_36, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_37': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_37, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_38': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_38, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_39': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_39, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_40': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_40, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_41': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_41, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_42': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_42, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_43': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_43, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_44': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_44, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_45': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_45, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_46': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_46, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_47': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_47, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_48': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_48, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_49': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_49, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_50': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_50, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_51': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_51, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_52': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_52, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_53': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_53, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_54': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_54, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_55': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_55, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_56': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_56, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_57': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_57, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_58': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_58, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_59': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_59, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_60': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_60, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_61': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_61, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_62': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_62, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_63': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_63, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_64': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_64, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_65': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_65, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_66': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_66, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_67': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_67, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_68': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_68, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_69': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_69, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_70': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_70, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_71': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_71, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_72': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_72, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_73': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_73, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_74': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_74, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_75': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_75, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_76': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_76, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_77': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_77, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_78': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_78, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_79': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_79, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_80': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_80, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_81': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_81, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_82': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_82, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_83': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_83, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_84': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_84, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_85': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_85, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_86': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_86, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_87': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_87, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_88': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_88, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_89': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_89, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_90': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_90, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_91': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_91, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_92': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_92, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_93': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_93, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_94': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_94, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_95': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_95, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_96': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_96, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_97': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_97, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_98': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_98, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_99': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_99, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_100': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_100, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_101': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_101, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_102': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_102, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_103': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_103, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_104': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_104, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_105': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_105, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_106': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_106, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_107': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_107, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_108': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_108, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_109': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_109, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_110': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_110, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_111': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_111, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_112': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_112, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_113': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_113, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_114': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_114, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_115': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_115, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_116': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_116, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_117': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_117, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_118': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_118, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_119': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_119, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_120': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_120, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_121': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_121, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_122': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_122, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_123': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_123, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_124': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_124, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_125': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_125, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_126': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_126, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_127': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_127, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_128': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_128, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_129': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_129, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_130': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_130, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_131': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_131, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_132': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_132, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_133': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_133, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_134': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_134, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_135': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_135, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_136': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_136, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_137': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_137, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_138': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_138, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_139': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_139, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_140': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_140, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_141': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_141, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_142': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_142, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_143': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_143, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_144': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_144, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_145': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_145, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_146': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_146, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_147': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_147, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_148': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_148, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_149': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_149, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_150': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_150, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_151': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_151, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_152': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_152, 
        'xǁCustomProgressBarǁ_draw_circular_bar__mutmut_153': xǁCustomProgressBarǁ_draw_circular_bar__mutmut_153
    }
    xǁCustomProgressBarǁ_draw_circular_bar__mutmut_orig.__name__ = 'xǁCustomProgressBarǁ_draw_circular_bar'

    def paintEvent(self, _) -> None:
        args = [_]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁCustomProgressBarǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁCustomProgressBarǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁCustomProgressBarǁpaintEvent__mutmut_orig(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._pixmap_cached, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_1(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._pixmap_cached, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_2(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._pixmap_cached, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_3(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._pixmap_cached, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_4(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(None)
        self._draw_cached_pixmap(painter, self._pixmap_cached, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_5(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(None, self._pixmap_cached, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_6(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, None, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_7(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._pixmap_cached, None)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_8(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(self._pixmap_cached, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_9(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._inner_rect)
        painter.end()

    def xǁCustomProgressBarǁpaintEvent__mutmut_10(self, _) -> None:
        """Re-implemented method, paint widget"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self._draw_circular_bar(painter)
        self._draw_cached_pixmap(painter, self._pixmap_cached, )
        painter.end()
    
    xǁCustomProgressBarǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁCustomProgressBarǁpaintEvent__mutmut_1': xǁCustomProgressBarǁpaintEvent__mutmut_1, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_2': xǁCustomProgressBarǁpaintEvent__mutmut_2, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_3': xǁCustomProgressBarǁpaintEvent__mutmut_3, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_4': xǁCustomProgressBarǁpaintEvent__mutmut_4, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_5': xǁCustomProgressBarǁpaintEvent__mutmut_5, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_6': xǁCustomProgressBarǁpaintEvent__mutmut_6, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_7': xǁCustomProgressBarǁpaintEvent__mutmut_7, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_8': xǁCustomProgressBarǁpaintEvent__mutmut_8, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_9': xǁCustomProgressBarǁpaintEvent__mutmut_9, 
        'xǁCustomProgressBarǁpaintEvent__mutmut_10': xǁCustomProgressBarǁpaintEvent__mutmut_10
    }
    xǁCustomProgressBarǁpaintEvent__mutmut_orig.__name__ = 'xǁCustomProgressBarǁpaintEvent'
