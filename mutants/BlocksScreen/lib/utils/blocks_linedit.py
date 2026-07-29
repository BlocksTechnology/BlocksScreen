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


class BlocksCustomLinEdit(QtWidgets.QLineEdit):
    clicked = QtCore.pyqtSignal()

    # Layout constants
    TEXT_MARGIN = 10
    CORNER_RADIUS = 8

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomLinEditǁ__init____mutmut_orig(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_1(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(None)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_2(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = None
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_3(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "XXType hereXX"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_4(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_5(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "TYPE HERE"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_6(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = None
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_7(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = "XXXX"
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_8(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = None  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_9(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = True  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_10(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = None
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_11(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = True
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_12(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = None

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_13(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = True

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_14(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = None
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_15(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(None, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_16(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, None, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_17(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, None)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_18(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_19(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_20(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, )
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_21(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(224, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_22(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 224, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_23(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 224)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_24(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = None
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_25(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(None, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_26(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, None, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_27(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, None)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_28(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_29(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_30(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, )
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_31(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(201, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_32(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 201, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_33(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 201)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_34(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = None
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_35(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(None, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_36(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, None, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_37(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, None)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_38(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_39(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_40(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, )
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_41(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(1, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_42(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 1, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_43(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 1)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_44(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = None

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_45(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(None, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_46(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, None, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_47(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, None)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_48(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_49(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_50(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, )

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_51(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(131, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_52(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 131, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_53(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 131)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_54(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(None, True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_55(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, None)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_56(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(True)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_57(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, )

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_58(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, False)

        # Cursor
        self.setCursor(QtCore.Qt.CursorShape.BlankCursor)

    def xǁBlocksCustomLinEditǁ__init____mutmut_59(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        # State
        self._placeholder_str = "Type here"
        self._name = ""
        self._secret = False  # True = show bullets, False = show text
        self._show_toggle = False
        self._is_password_visible = False

        # Pre-allocated colors (avoid allocation in paint)
        self._bg_color = QtGui.QColor(223, 223, 223)
        self._bg_pressed_color = QtGui.QColor(200, 200, 200)
        self._text_color = QtGui.QColor(0, 0, 0)
        self._placeholder_color = QtGui.QColor(130, 130, 130)

        # Touch support
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

        # Cursor
        self.setCursor(None)
    
    xǁBlocksCustomLinEditǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁ__init____mutmut_1': xǁBlocksCustomLinEditǁ__init____mutmut_1, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_2': xǁBlocksCustomLinEditǁ__init____mutmut_2, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_3': xǁBlocksCustomLinEditǁ__init____mutmut_3, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_4': xǁBlocksCustomLinEditǁ__init____mutmut_4, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_5': xǁBlocksCustomLinEditǁ__init____mutmut_5, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_6': xǁBlocksCustomLinEditǁ__init____mutmut_6, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_7': xǁBlocksCustomLinEditǁ__init____mutmut_7, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_8': xǁBlocksCustomLinEditǁ__init____mutmut_8, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_9': xǁBlocksCustomLinEditǁ__init____mutmut_9, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_10': xǁBlocksCustomLinEditǁ__init____mutmut_10, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_11': xǁBlocksCustomLinEditǁ__init____mutmut_11, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_12': xǁBlocksCustomLinEditǁ__init____mutmut_12, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_13': xǁBlocksCustomLinEditǁ__init____mutmut_13, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_14': xǁBlocksCustomLinEditǁ__init____mutmut_14, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_15': xǁBlocksCustomLinEditǁ__init____mutmut_15, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_16': xǁBlocksCustomLinEditǁ__init____mutmut_16, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_17': xǁBlocksCustomLinEditǁ__init____mutmut_17, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_18': xǁBlocksCustomLinEditǁ__init____mutmut_18, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_19': xǁBlocksCustomLinEditǁ__init____mutmut_19, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_20': xǁBlocksCustomLinEditǁ__init____mutmut_20, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_21': xǁBlocksCustomLinEditǁ__init____mutmut_21, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_22': xǁBlocksCustomLinEditǁ__init____mutmut_22, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_23': xǁBlocksCustomLinEditǁ__init____mutmut_23, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_24': xǁBlocksCustomLinEditǁ__init____mutmut_24, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_25': xǁBlocksCustomLinEditǁ__init____mutmut_25, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_26': xǁBlocksCustomLinEditǁ__init____mutmut_26, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_27': xǁBlocksCustomLinEditǁ__init____mutmut_27, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_28': xǁBlocksCustomLinEditǁ__init____mutmut_28, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_29': xǁBlocksCustomLinEditǁ__init____mutmut_29, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_30': xǁBlocksCustomLinEditǁ__init____mutmut_30, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_31': xǁBlocksCustomLinEditǁ__init____mutmut_31, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_32': xǁBlocksCustomLinEditǁ__init____mutmut_32, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_33': xǁBlocksCustomLinEditǁ__init____mutmut_33, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_34': xǁBlocksCustomLinEditǁ__init____mutmut_34, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_35': xǁBlocksCustomLinEditǁ__init____mutmut_35, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_36': xǁBlocksCustomLinEditǁ__init____mutmut_36, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_37': xǁBlocksCustomLinEditǁ__init____mutmut_37, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_38': xǁBlocksCustomLinEditǁ__init____mutmut_38, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_39': xǁBlocksCustomLinEditǁ__init____mutmut_39, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_40': xǁBlocksCustomLinEditǁ__init____mutmut_40, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_41': xǁBlocksCustomLinEditǁ__init____mutmut_41, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_42': xǁBlocksCustomLinEditǁ__init____mutmut_42, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_43': xǁBlocksCustomLinEditǁ__init____mutmut_43, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_44': xǁBlocksCustomLinEditǁ__init____mutmut_44, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_45': xǁBlocksCustomLinEditǁ__init____mutmut_45, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_46': xǁBlocksCustomLinEditǁ__init____mutmut_46, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_47': xǁBlocksCustomLinEditǁ__init____mutmut_47, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_48': xǁBlocksCustomLinEditǁ__init____mutmut_48, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_49': xǁBlocksCustomLinEditǁ__init____mutmut_49, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_50': xǁBlocksCustomLinEditǁ__init____mutmut_50, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_51': xǁBlocksCustomLinEditǁ__init____mutmut_51, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_52': xǁBlocksCustomLinEditǁ__init____mutmut_52, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_53': xǁBlocksCustomLinEditǁ__init____mutmut_53, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_54': xǁBlocksCustomLinEditǁ__init____mutmut_54, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_55': xǁBlocksCustomLinEditǁ__init____mutmut_55, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_56': xǁBlocksCustomLinEditǁ__init____mutmut_56, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_57': xǁBlocksCustomLinEditǁ__init____mutmut_57, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_58': xǁBlocksCustomLinEditǁ__init____mutmut_58, 
        'xǁBlocksCustomLinEditǁ__init____mutmut_59': xǁBlocksCustomLinEditǁ__init____mutmut_59
    }
    xǁBlocksCustomLinEditǁ__init____mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁ__init__'

    @property
    def name(self) -> str:
        """Widget name property."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.setObjectName(value)

    def placeholderText(self) -> str:
        """Get placeholder text."""
        return self._placeholder_str

    def setPlaceholderText(self, text: str) -> None:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_orig(self, text: str) -> None:
        """Set placeholder text displayed when empty."""
        self._placeholder_str = text
        self.update()

    def xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_1(self, text: str) -> None:
        """Set placeholder text displayed when empty."""
        self._placeholder_str = None
        self.update()
    
    xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_1': xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_1
    }
    xǁBlocksCustomLinEditǁsetPlaceholderText__mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁsetPlaceholderText'

    def showToggleButton(self) -> bool:
        """Check if toggle button is enabled."""
        return self._show_toggle

    def setHidden(self, hidden: bool) -> None:
        args = [hidden]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁsetHidden__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁsetHidden__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomLinEditǁsetHidden__mutmut_orig(self, hidden: bool) -> None:
        """
        Set whether text is hidden (password mode).

        Args:
            hidden: True to show bullets, False to show actual text
        """
        if self._secret == hidden:
            return

        self._secret = hidden
        self._is_password_visible = not hidden
        self.update()

    def xǁBlocksCustomLinEditǁsetHidden__mutmut_1(self, hidden: bool) -> None:
        """
        Set whether text is hidden (password mode).

        Args:
            hidden: True to show bullets, False to show actual text
        """
        if self._secret != hidden:
            return

        self._secret = hidden
        self._is_password_visible = not hidden
        self.update()

    def xǁBlocksCustomLinEditǁsetHidden__mutmut_2(self, hidden: bool) -> None:
        """
        Set whether text is hidden (password mode).

        Args:
            hidden: True to show bullets, False to show actual text
        """
        if self._secret == hidden:
            return

        self._secret = None
        self._is_password_visible = not hidden
        self.update()

    def xǁBlocksCustomLinEditǁsetHidden__mutmut_3(self, hidden: bool) -> None:
        """
        Set whether text is hidden (password mode).

        Args:
            hidden: True to show bullets, False to show actual text
        """
        if self._secret == hidden:
            return

        self._secret = hidden
        self._is_password_visible = None
        self.update()

    def xǁBlocksCustomLinEditǁsetHidden__mutmut_4(self, hidden: bool) -> None:
        """
        Set whether text is hidden (password mode).

        Args:
            hidden: True to show bullets, False to show actual text
        """
        if self._secret == hidden:
            return

        self._secret = hidden
        self._is_password_visible = hidden
        self.update()
    
    xǁBlocksCustomLinEditǁsetHidden__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁsetHidden__mutmut_1': xǁBlocksCustomLinEditǁsetHidden__mutmut_1, 
        'xǁBlocksCustomLinEditǁsetHidden__mutmut_2': xǁBlocksCustomLinEditǁsetHidden__mutmut_2, 
        'xǁBlocksCustomLinEditǁsetHidden__mutmut_3': xǁBlocksCustomLinEditǁsetHidden__mutmut_3, 
        'xǁBlocksCustomLinEditǁsetHidden__mutmut_4': xǁBlocksCustomLinEditǁsetHidden__mutmut_4
    }
    xǁBlocksCustomLinEditǁsetHidden__mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁsetHidden'

    def isPasswordVisible(self) -> bool:
        """Check if password is currently visible."""
        return self._is_password_visible

    def _get_text_rect(self) -> QtCore.QRect:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_orig(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_1(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = None
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_2(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = None

        return self.rect().adjusted(left_margin, 0, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_3(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(None, 0, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_4(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, None, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_5(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, None, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_6(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, -right_margin, None)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_7(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(0, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_8(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_9(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_10(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, -right_margin, )

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_11(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 1, -right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_12(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, +right_margin, 0)

    def xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_13(self) -> QtCore.QRect:
        """Calculate the rectangle available for text rendering."""
        left_margin = self.TEXT_MARGIN
        right_margin = self.TEXT_MARGIN

        return self.rect().adjusted(left_margin, 0, -right_margin, 1)
    
    xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_1': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_1, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_2': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_2, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_3': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_3, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_4': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_4, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_5': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_5, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_6': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_6, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_7': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_7, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_8': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_8, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_9': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_9, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_10': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_10, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_11': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_11, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_12': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_12, 
        'xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_13': xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_13
    }
    xǁBlocksCustomLinEditǁ_get_text_rect__mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁ_get_text_rect'

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁmousePressEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁmousePressEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomLinEditǁmousePressEvent__mutmut_orig(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse press"""
        self.clicked.emit()
        super().mousePressEvent(event)

    def xǁBlocksCustomLinEditǁmousePressEvent__mutmut_1(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse press"""
        self.clicked.emit()
        super().mousePressEvent(None)
    
    xǁBlocksCustomLinEditǁmousePressEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁmousePressEvent__mutmut_1': xǁBlocksCustomLinEditǁmousePressEvent__mutmut_1
    }
    xǁBlocksCustomLinEditǁmousePressEvent__mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁmousePressEvent'

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_orig(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse release"""
        super().mouseReleaseEvent(event)

    def xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_1(self, event: QtGui.QMouseEvent) -> None:
        """Handle mouse release"""
        super().mouseReleaseEvent(None)
    
    xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_1': xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_1
    }
    xǁBlocksCustomLinEditǁmouseReleaseEvent__mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁmouseReleaseEvent'



    def paintEvent(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁpaintEvent__mutmut_mutants'), args, kwargs, self)



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_orig(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_1(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_2(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_3(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_4(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, None)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_5(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_6(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, )

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_7(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, False)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_8(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(None)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_9(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(None)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_10(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(None, self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_11(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), None, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_12(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, None)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_13(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_14(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS)

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_15(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, )

        # Text
        self._draw_text(painter)

        painter.end()



    def xǁBlocksCustomLinEditǁpaintEvent__mutmut_16(self, event: typing.Optional[QtGui.QPaintEvent]) -> None:
        """Custom paint with embedded toggle button."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.CORNER_RADIUS, self.CORNER_RADIUS)

        # Text
        self._draw_text(None)

        painter.end()
    
    xǁBlocksCustomLinEditǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁpaintEvent__mutmut_1': xǁBlocksCustomLinEditǁpaintEvent__mutmut_1, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_2': xǁBlocksCustomLinEditǁpaintEvent__mutmut_2, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_3': xǁBlocksCustomLinEditǁpaintEvent__mutmut_3, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_4': xǁBlocksCustomLinEditǁpaintEvent__mutmut_4, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_5': xǁBlocksCustomLinEditǁpaintEvent__mutmut_5, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_6': xǁBlocksCustomLinEditǁpaintEvent__mutmut_6, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_7': xǁBlocksCustomLinEditǁpaintEvent__mutmut_7, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_8': xǁBlocksCustomLinEditǁpaintEvent__mutmut_8, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_9': xǁBlocksCustomLinEditǁpaintEvent__mutmut_9, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_10': xǁBlocksCustomLinEditǁpaintEvent__mutmut_10, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_11': xǁBlocksCustomLinEditǁpaintEvent__mutmut_11, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_12': xǁBlocksCustomLinEditǁpaintEvent__mutmut_12, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_13': xǁBlocksCustomLinEditǁpaintEvent__mutmut_13, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_14': xǁBlocksCustomLinEditǁpaintEvent__mutmut_14, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_15': xǁBlocksCustomLinEditǁpaintEvent__mutmut_15, 
        'xǁBlocksCustomLinEditǁpaintEvent__mutmut_16': xǁBlocksCustomLinEditǁpaintEvent__mutmut_16
    }
    xǁBlocksCustomLinEditǁpaintEvent__mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁpaintEvent'

    def _draw_text(self, painter: QtGui.QPainter) -> None:
        args = [painter]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBlocksCustomLinEditǁ_draw_text__mutmut_orig'), object.__getattribute__(self, 'xǁBlocksCustomLinEditǁ_draw_text__mutmut_mutants'), args, kwargs, self)

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_orig(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_1(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = None
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_2(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = None

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_3(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret or display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_4(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = None

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_5(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" / len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_6(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "XX*XX" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_7(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(None)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_8(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(None)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_9(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                None,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_10(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                None,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_11(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                None,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_12(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_13(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_14(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_15(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft & QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_16(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(None)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_17(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(None)
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_18(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                None,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_19(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                None,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_20(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                None,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_21(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_22(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                self._placeholder_str,
            )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_23(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                )

    def xǁBlocksCustomLinEditǁ_draw_text__mutmut_24(self, painter: QtGui.QPainter) -> None:
        """Draw the text or placeholder."""
        text_rect = self._get_text_rect()
        display_text = self.text()

        # Apply password masking
        if self._secret and display_text:
            display_text = "*" * len(display_text)

        if display_text:
            painter.setPen(self._text_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft
                | QtCore.Qt.AlignmentFlag.AlignVCenter,
                display_text,
            )
        else:
            # Placeholder text
            painter.setPen(self._placeholder_color)
            painter.setFont(self.font())
            painter.drawText(
                text_rect,
                QtCore.Qt.AlignmentFlag.AlignLeft & QtCore.Qt.AlignmentFlag.AlignVCenter,
                self._placeholder_str,
            )
    
    xǁBlocksCustomLinEditǁ_draw_text__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBlocksCustomLinEditǁ_draw_text__mutmut_1': xǁBlocksCustomLinEditǁ_draw_text__mutmut_1, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_2': xǁBlocksCustomLinEditǁ_draw_text__mutmut_2, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_3': xǁBlocksCustomLinEditǁ_draw_text__mutmut_3, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_4': xǁBlocksCustomLinEditǁ_draw_text__mutmut_4, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_5': xǁBlocksCustomLinEditǁ_draw_text__mutmut_5, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_6': xǁBlocksCustomLinEditǁ_draw_text__mutmut_6, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_7': xǁBlocksCustomLinEditǁ_draw_text__mutmut_7, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_8': xǁBlocksCustomLinEditǁ_draw_text__mutmut_8, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_9': xǁBlocksCustomLinEditǁ_draw_text__mutmut_9, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_10': xǁBlocksCustomLinEditǁ_draw_text__mutmut_10, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_11': xǁBlocksCustomLinEditǁ_draw_text__mutmut_11, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_12': xǁBlocksCustomLinEditǁ_draw_text__mutmut_12, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_13': xǁBlocksCustomLinEditǁ_draw_text__mutmut_13, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_14': xǁBlocksCustomLinEditǁ_draw_text__mutmut_14, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_15': xǁBlocksCustomLinEditǁ_draw_text__mutmut_15, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_16': xǁBlocksCustomLinEditǁ_draw_text__mutmut_16, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_17': xǁBlocksCustomLinEditǁ_draw_text__mutmut_17, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_18': xǁBlocksCustomLinEditǁ_draw_text__mutmut_18, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_19': xǁBlocksCustomLinEditǁ_draw_text__mutmut_19, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_20': xǁBlocksCustomLinEditǁ_draw_text__mutmut_20, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_21': xǁBlocksCustomLinEditǁ_draw_text__mutmut_21, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_22': xǁBlocksCustomLinEditǁ_draw_text__mutmut_22, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_23': xǁBlocksCustomLinEditǁ_draw_text__mutmut_23, 
        'xǁBlocksCustomLinEditǁ_draw_text__mutmut_24': xǁBlocksCustomLinEditǁ_draw_text__mutmut_24
    }
    xǁBlocksCustomLinEditǁ_draw_text__mutmut_orig.__name__ = 'xǁBlocksCustomLinEditǁ_draw_text'
