from PyQt6 import QtCore, QtWidgets
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


class FansPage(QtWidgets.QWidget):
    def __init__(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        args = [parent, flags]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFansPageǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁFansPageǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁFansPageǁ__init____mutmut_orig(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_1(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None or flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_2(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is None and flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_3(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_4(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(None, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_5(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, None)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_6(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_7(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, )

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_8(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(None, self).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_9(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, None).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_10(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(self).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_11(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, ).__init__(parent, flags)

        else:
            super(FansPage, self).__init__()
    def xǁFansPageǁ__init____mutmut_12(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(None, self).__init__()
    def xǁFansPageǁ__init____mutmut_13(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(FansPage, None).__init__()
    def xǁFansPageǁ__init____mutmut_14(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(self).__init__()
    def xǁFansPageǁ__init____mutmut_15(
        self,
        parent: typing.Optional["QtWidgets.QWidget"],
        flags: typing.Optional["QtCore.Qt.WindowType"],
    ) -> None:
        if parent is not None and flags is not None:
            super(FansPage, self).__init__(parent, flags)

        else:
            super(FansPage, ).__init__()
    
    xǁFansPageǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFansPageǁ__init____mutmut_1': xǁFansPageǁ__init____mutmut_1, 
        'xǁFansPageǁ__init____mutmut_2': xǁFansPageǁ__init____mutmut_2, 
        'xǁFansPageǁ__init____mutmut_3': xǁFansPageǁ__init____mutmut_3, 
        'xǁFansPageǁ__init____mutmut_4': xǁFansPageǁ__init____mutmut_4, 
        'xǁFansPageǁ__init____mutmut_5': xǁFansPageǁ__init____mutmut_5, 
        'xǁFansPageǁ__init____mutmut_6': xǁFansPageǁ__init____mutmut_6, 
        'xǁFansPageǁ__init____mutmut_7': xǁFansPageǁ__init____mutmut_7, 
        'xǁFansPageǁ__init____mutmut_8': xǁFansPageǁ__init____mutmut_8, 
        'xǁFansPageǁ__init____mutmut_9': xǁFansPageǁ__init____mutmut_9, 
        'xǁFansPageǁ__init____mutmut_10': xǁFansPageǁ__init____mutmut_10, 
        'xǁFansPageǁ__init____mutmut_11': xǁFansPageǁ__init____mutmut_11, 
        'xǁFansPageǁ__init____mutmut_12': xǁFansPageǁ__init____mutmut_12, 
        'xǁFansPageǁ__init____mutmut_13': xǁFansPageǁ__init____mutmut_13, 
        'xǁFansPageǁ__init____mutmut_14': xǁFansPageǁ__init____mutmut_14, 
        'xǁFansPageǁ__init____mutmut_15': xǁFansPageǁ__init____mutmut_15
    }
    xǁFansPageǁ__init____mutmut_orig.__name__ = 'xǁFansPageǁ__init__'
