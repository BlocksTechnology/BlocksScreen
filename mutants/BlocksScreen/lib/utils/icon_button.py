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


class IconButton(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁIconButtonǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁIconButtonǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁIconButtonǁ__init____mutmut_orig(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_1(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(None)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_2(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = None
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_3(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = None
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_4(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = "XXXX"
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_5(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = None
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_6(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = True
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_7(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = None
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_8(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = "XXXX"
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_9(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = None
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_10(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = "XXXX"
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_11(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_12(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(None, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_13(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, None, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_14(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, None)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_15(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_16(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_17(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_18(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(256, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_19(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 256, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_20(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 256)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_21(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(None, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_22(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, None)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_23(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_24(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, )
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_25(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, False)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_26(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = None  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_27(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(None, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_28(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, None, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_29(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, None, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_30(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, None)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_31(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_32(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_33(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_34(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, )  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_35(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(224, 223, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_36(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 224, 223, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_37(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 224, 70)  # Set to solid white
    def xǁIconButtonǁ__init____mutmut_38(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)

        self.icon_pixmap: QtGui.QPixmap = QtGui.QPixmap()
        self.text_formatting: str = ""
        self.has_text: bool = False
        self._text: str = ""
        self._name: str = ""
        self.text_color: QtGui.QColor = QtGui.QColor(255, 255, 255)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.pressed_bg_color = QtGui.QColor(223, 223, 223, 71)  # Set to solid white
    
    xǁIconButtonǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁIconButtonǁ__init____mutmut_1': xǁIconButtonǁ__init____mutmut_1, 
        'xǁIconButtonǁ__init____mutmut_2': xǁIconButtonǁ__init____mutmut_2, 
        'xǁIconButtonǁ__init____mutmut_3': xǁIconButtonǁ__init____mutmut_3, 
        'xǁIconButtonǁ__init____mutmut_4': xǁIconButtonǁ__init____mutmut_4, 
        'xǁIconButtonǁ__init____mutmut_5': xǁIconButtonǁ__init____mutmut_5, 
        'xǁIconButtonǁ__init____mutmut_6': xǁIconButtonǁ__init____mutmut_6, 
        'xǁIconButtonǁ__init____mutmut_7': xǁIconButtonǁ__init____mutmut_7, 
        'xǁIconButtonǁ__init____mutmut_8': xǁIconButtonǁ__init____mutmut_8, 
        'xǁIconButtonǁ__init____mutmut_9': xǁIconButtonǁ__init____mutmut_9, 
        'xǁIconButtonǁ__init____mutmut_10': xǁIconButtonǁ__init____mutmut_10, 
        'xǁIconButtonǁ__init____mutmut_11': xǁIconButtonǁ__init____mutmut_11, 
        'xǁIconButtonǁ__init____mutmut_12': xǁIconButtonǁ__init____mutmut_12, 
        'xǁIconButtonǁ__init____mutmut_13': xǁIconButtonǁ__init____mutmut_13, 
        'xǁIconButtonǁ__init____mutmut_14': xǁIconButtonǁ__init____mutmut_14, 
        'xǁIconButtonǁ__init____mutmut_15': xǁIconButtonǁ__init____mutmut_15, 
        'xǁIconButtonǁ__init____mutmut_16': xǁIconButtonǁ__init____mutmut_16, 
        'xǁIconButtonǁ__init____mutmut_17': xǁIconButtonǁ__init____mutmut_17, 
        'xǁIconButtonǁ__init____mutmut_18': xǁIconButtonǁ__init____mutmut_18, 
        'xǁIconButtonǁ__init____mutmut_19': xǁIconButtonǁ__init____mutmut_19, 
        'xǁIconButtonǁ__init____mutmut_20': xǁIconButtonǁ__init____mutmut_20, 
        'xǁIconButtonǁ__init____mutmut_21': xǁIconButtonǁ__init____mutmut_21, 
        'xǁIconButtonǁ__init____mutmut_22': xǁIconButtonǁ__init____mutmut_22, 
        'xǁIconButtonǁ__init____mutmut_23': xǁIconButtonǁ__init____mutmut_23, 
        'xǁIconButtonǁ__init____mutmut_24': xǁIconButtonǁ__init____mutmut_24, 
        'xǁIconButtonǁ__init____mutmut_25': xǁIconButtonǁ__init____mutmut_25, 
        'xǁIconButtonǁ__init____mutmut_26': xǁIconButtonǁ__init____mutmut_26, 
        'xǁIconButtonǁ__init____mutmut_27': xǁIconButtonǁ__init____mutmut_27, 
        'xǁIconButtonǁ__init____mutmut_28': xǁIconButtonǁ__init____mutmut_28, 
        'xǁIconButtonǁ__init____mutmut_29': xǁIconButtonǁ__init____mutmut_29, 
        'xǁIconButtonǁ__init____mutmut_30': xǁIconButtonǁ__init____mutmut_30, 
        'xǁIconButtonǁ__init____mutmut_31': xǁIconButtonǁ__init____mutmut_31, 
        'xǁIconButtonǁ__init____mutmut_32': xǁIconButtonǁ__init____mutmut_32, 
        'xǁIconButtonǁ__init____mutmut_33': xǁIconButtonǁ__init____mutmut_33, 
        'xǁIconButtonǁ__init____mutmut_34': xǁIconButtonǁ__init____mutmut_34, 
        'xǁIconButtonǁ__init____mutmut_35': xǁIconButtonǁ__init____mutmut_35, 
        'xǁIconButtonǁ__init____mutmut_36': xǁIconButtonǁ__init____mutmut_36, 
        'xǁIconButtonǁ__init____mutmut_37': xǁIconButtonǁ__init____mutmut_37, 
        'xǁIconButtonǁ__init____mutmut_38': xǁIconButtonǁ__init____mutmut_38
    }
    xǁIconButtonǁ__init____mutmut_orig.__name__ = 'xǁIconButtonǁ__init__'

    @property
    def name(self):
        """Widget name"""
        return self._name

    def text(self) -> str:
        """Widget text"""
        return self._text

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        args = [pixmap]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁIconButtonǁsetPixmap__mutmut_orig'), object.__getattribute__(self, 'xǁIconButtonǁsetPixmap__mutmut_mutants'), args, kwargs, self)

    def xǁIconButtonǁsetPixmap__mutmut_orig(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = pixmap
        self.repaint()

    def xǁIconButtonǁsetPixmap__mutmut_1(self, pixmap: QtGui.QPixmap) -> None:
        """Set widget pixmap"""
        self.icon_pixmap = None
        self.repaint()
    
    xǁIconButtonǁsetPixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁIconButtonǁsetPixmap__mutmut_1': xǁIconButtonǁsetPixmap__mutmut_1
    }
    xǁIconButtonǁsetPixmap__mutmut_orig.__name__ = 'xǁIconButtonǁsetPixmap'

    def clearPixmap(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁIconButtonǁclearPixmap__mutmut_orig'), object.__getattribute__(self, 'xǁIconButtonǁclearPixmap__mutmut_mutants'), args, kwargs, self)

    def xǁIconButtonǁclearPixmap__mutmut_orig(self) -> None:
        """Clear widget pixmap"""
        self.icon_pixmap = QtGui.QPixmap()
        self.repaint()

    def xǁIconButtonǁclearPixmap__mutmut_1(self) -> None:
        """Clear widget pixmap"""
        self.icon_pixmap = None
        self.repaint()
    
    xǁIconButtonǁclearPixmap__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁIconButtonǁclearPixmap__mutmut_1': xǁIconButtonǁclearPixmap__mutmut_1
    }
    xǁIconButtonǁclearPixmap__mutmut_orig.__name__ = 'xǁIconButtonǁclearPixmap'

    def setText(self, text: str) -> None:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁIconButtonǁsetText__mutmut_orig'), object.__getattribute__(self, 'xǁIconButtonǁsetText__mutmut_mutants'), args, kwargs, self)

    def xǁIconButtonǁsetText__mutmut_orig(self, text: str) -> None:
        """Set widget text"""
        self._text = text
        self.update()

    def xǁIconButtonǁsetText__mutmut_1(self, text: str) -> None:
        """Set widget text"""
        self._text = None
        self.update()
    
    xǁIconButtonǁsetText__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁIconButtonǁsetText__mutmut_1': xǁIconButtonǁsetText__mutmut_1
    }
    xǁIconButtonǁsetText__mutmut_orig.__name__ = 'xǁIconButtonǁsetText'

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁIconButtonǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁIconButtonǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁIconButtonǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = None
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(None)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = None
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(None)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(None, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, None)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, )
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, False)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(None, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, None)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, )
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, False)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(None, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, None)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, )

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, False)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(None)
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(None))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(None)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(None, 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), None, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, None)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, )
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 7, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 7)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = None
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(None)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(None)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(None)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(1.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(None)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = None
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 16.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 6.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = None
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                None, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, None, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, None, (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_44(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), None
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_45(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_46(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_47(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_48(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_49(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                3.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_50(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 3.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_51(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() + 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_52(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 6), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_53(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 + y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_54(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() + 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_55(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 6 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_56(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = None

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_57(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(None, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_58(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, None, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_59(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, None, (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_60(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), None)

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_61(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_62(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_63(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_64(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), )

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_65(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(1.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_66(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 1.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_67(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() + y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_68(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_69(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = None
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_70(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                None,
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_71(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                None,
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_72(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                None,
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_73(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_74(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_75(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_76(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = None
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_77(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = None
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_78(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = None
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_79(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) * 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_80(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() + scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_81(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 3.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_82(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = None
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_83(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) * 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_84(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() + scaled_height) / 2.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_85(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 3.0
            adjusted_icon_rect = QtCore.QRectF(
                _icon_rect.x() + adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_86(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
            _icon_scaled = self.icon_pixmap.scaled(
                _icon_rect.size().toSize(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled_width = _icon_scaled.width()
            scaled_height = _icon_scaled.height()
            adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
            adjusted_y = (_icon_rect.height() - scaled_height) / 2.0
            adjusted_icon_rect = None

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_87(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                None,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_88(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                None,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_89(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                None,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_90(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                None,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_91(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_92(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_93(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_94(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_95(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                _icon_rect.x() - adjusted_x,
                _icon_rect.y() + adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_96(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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
                _icon_rect.y() - adjusted_y,
                scaled_width,
                scaled_height,
            )

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_97(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                None,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_98(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                None,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_99(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                None,
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_100(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_101(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_102(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_103(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                None
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_104(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_105(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = None
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_106(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = None
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_107(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = None
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_108(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) * 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_109(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() + scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_110(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 3.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_111(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = None

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_112(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) * 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_113(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() + scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_114(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 3.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_115(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = None
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_116(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    None,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_117(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    None,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_118(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    None,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_119(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    None,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_120(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_121(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_122(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_123(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_124(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() - adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_125(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() - adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_126(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting != "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_127(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "XXbottomXX":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_128(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "BOTTOM":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_129(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = None

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_130(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    None,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_131(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    None,
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_132(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    None,
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_133(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    None,
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_134(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_135(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_136(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_137(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_138(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    1,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_139(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() + _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_140(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(None)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_141(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(None)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_142(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                None,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_143(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                None,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_144(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                None,
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_145(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_146(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_147(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_148(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine & QtCore.Qt.AlignmentFlag.AlignCenter,
                str(self.text()),
            )

        painter.end()

    def xǁIconButtonǁpaintEvent__mutmut_149(self, a0: QtGui.QPaintEvent) -> None:
        """Re-implemented method, paint widget"""
        opt = QtWidgets.QStyleOptionButton()
        self.initStyleOption(opt)
        painter = QtWidgets.QStylePainter(self)
        painter.setRenderHint(painter.RenderHint.Antialiasing, True)
        painter.setRenderHint(painter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(painter.RenderHint.LosslessImageRendering, True)

        if self.isDown():
            painter.setBrush(QtGui.QBrush(self.pressed_bg_color))
            painter.setPen(QtCore.Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().toRectF(), 6, 6)
        _pen = QtGui.QPen()
        _pen.setStyle(QtCore.Qt.PenStyle.NoPen)
        _pen.setColor(self.text_color)
        _pen.setWidthF(0.8)

        painter.setPen(_pen)

        y = 15.0 if self.text_formatting else 5.0
        if self.isDown():
            _icon_rect = QtCore.QRectF(
                2.5, 2.5, (self.width() - 5), (self.height() - 5 - y)
            )
        else:
            _icon_rect = QtCore.QRectF(0.0, 0.0, (self.width()), (self.height() - y))

        if not self.icon_pixmap.isNull():
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

            painter.drawPixmap(
                adjusted_icon_rect,
                _icon_scaled,
                _icon_scaled.rect().toRectF(),
            )

        if self.has_text:
            painter.setCompositionMode(
                painter.CompositionMode.CompositionMode_Difference
            )
            if not self.text_formatting:
                scaled_width = _icon_rect.width()
                scaled_height = _icon_rect.height()
                adjusted_x = (_icon_rect.width() - scaled_width) / 2.0
                adjusted_y = (_icon_rect.height() - scaled_height) / 2.0

                adjusted_rectF = QtCore.QRectF(
                    _icon_rect.x() + adjusted_x,
                    _icon_rect.y() + adjusted_y,
                    scaled_width,
                    scaled_height,
                )
            elif self.text_formatting == "bottom":
                # adjusted_x = 0#(_icon_rect.width() - self.width() + 5.0) / 2.0
                adjusted_rectF = QtCore.QRectF(
                    0,
                    _icon_rect.height(),
                    self.width(),
                    self.height() - _icon_rect.height(),
                )

            _pen.setStyle(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(_pen)

            painter.drawText(
                adjusted_rectF,
                QtCore.Qt.TextFlag.TextSingleLine | QtCore.Qt.AlignmentFlag.AlignCenter,
                str(None),
            )

        painter.end()
    
    xǁIconButtonǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁIconButtonǁpaintEvent__mutmut_1': xǁIconButtonǁpaintEvent__mutmut_1, 
        'xǁIconButtonǁpaintEvent__mutmut_2': xǁIconButtonǁpaintEvent__mutmut_2, 
        'xǁIconButtonǁpaintEvent__mutmut_3': xǁIconButtonǁpaintEvent__mutmut_3, 
        'xǁIconButtonǁpaintEvent__mutmut_4': xǁIconButtonǁpaintEvent__mutmut_4, 
        'xǁIconButtonǁpaintEvent__mutmut_5': xǁIconButtonǁpaintEvent__mutmut_5, 
        'xǁIconButtonǁpaintEvent__mutmut_6': xǁIconButtonǁpaintEvent__mutmut_6, 
        'xǁIconButtonǁpaintEvent__mutmut_7': xǁIconButtonǁpaintEvent__mutmut_7, 
        'xǁIconButtonǁpaintEvent__mutmut_8': xǁIconButtonǁpaintEvent__mutmut_8, 
        'xǁIconButtonǁpaintEvent__mutmut_9': xǁIconButtonǁpaintEvent__mutmut_9, 
        'xǁIconButtonǁpaintEvent__mutmut_10': xǁIconButtonǁpaintEvent__mutmut_10, 
        'xǁIconButtonǁpaintEvent__mutmut_11': xǁIconButtonǁpaintEvent__mutmut_11, 
        'xǁIconButtonǁpaintEvent__mutmut_12': xǁIconButtonǁpaintEvent__mutmut_12, 
        'xǁIconButtonǁpaintEvent__mutmut_13': xǁIconButtonǁpaintEvent__mutmut_13, 
        'xǁIconButtonǁpaintEvent__mutmut_14': xǁIconButtonǁpaintEvent__mutmut_14, 
        'xǁIconButtonǁpaintEvent__mutmut_15': xǁIconButtonǁpaintEvent__mutmut_15, 
        'xǁIconButtonǁpaintEvent__mutmut_16': xǁIconButtonǁpaintEvent__mutmut_16, 
        'xǁIconButtonǁpaintEvent__mutmut_17': xǁIconButtonǁpaintEvent__mutmut_17, 
        'xǁIconButtonǁpaintEvent__mutmut_18': xǁIconButtonǁpaintEvent__mutmut_18, 
        'xǁIconButtonǁpaintEvent__mutmut_19': xǁIconButtonǁpaintEvent__mutmut_19, 
        'xǁIconButtonǁpaintEvent__mutmut_20': xǁIconButtonǁpaintEvent__mutmut_20, 
        'xǁIconButtonǁpaintEvent__mutmut_21': xǁIconButtonǁpaintEvent__mutmut_21, 
        'xǁIconButtonǁpaintEvent__mutmut_22': xǁIconButtonǁpaintEvent__mutmut_22, 
        'xǁIconButtonǁpaintEvent__mutmut_23': xǁIconButtonǁpaintEvent__mutmut_23, 
        'xǁIconButtonǁpaintEvent__mutmut_24': xǁIconButtonǁpaintEvent__mutmut_24, 
        'xǁIconButtonǁpaintEvent__mutmut_25': xǁIconButtonǁpaintEvent__mutmut_25, 
        'xǁIconButtonǁpaintEvent__mutmut_26': xǁIconButtonǁpaintEvent__mutmut_26, 
        'xǁIconButtonǁpaintEvent__mutmut_27': xǁIconButtonǁpaintEvent__mutmut_27, 
        'xǁIconButtonǁpaintEvent__mutmut_28': xǁIconButtonǁpaintEvent__mutmut_28, 
        'xǁIconButtonǁpaintEvent__mutmut_29': xǁIconButtonǁpaintEvent__mutmut_29, 
        'xǁIconButtonǁpaintEvent__mutmut_30': xǁIconButtonǁpaintEvent__mutmut_30, 
        'xǁIconButtonǁpaintEvent__mutmut_31': xǁIconButtonǁpaintEvent__mutmut_31, 
        'xǁIconButtonǁpaintEvent__mutmut_32': xǁIconButtonǁpaintEvent__mutmut_32, 
        'xǁIconButtonǁpaintEvent__mutmut_33': xǁIconButtonǁpaintEvent__mutmut_33, 
        'xǁIconButtonǁpaintEvent__mutmut_34': xǁIconButtonǁpaintEvent__mutmut_34, 
        'xǁIconButtonǁpaintEvent__mutmut_35': xǁIconButtonǁpaintEvent__mutmut_35, 
        'xǁIconButtonǁpaintEvent__mutmut_36': xǁIconButtonǁpaintEvent__mutmut_36, 
        'xǁIconButtonǁpaintEvent__mutmut_37': xǁIconButtonǁpaintEvent__mutmut_37, 
        'xǁIconButtonǁpaintEvent__mutmut_38': xǁIconButtonǁpaintEvent__mutmut_38, 
        'xǁIconButtonǁpaintEvent__mutmut_39': xǁIconButtonǁpaintEvent__mutmut_39, 
        'xǁIconButtonǁpaintEvent__mutmut_40': xǁIconButtonǁpaintEvent__mutmut_40, 
        'xǁIconButtonǁpaintEvent__mutmut_41': xǁIconButtonǁpaintEvent__mutmut_41, 
        'xǁIconButtonǁpaintEvent__mutmut_42': xǁIconButtonǁpaintEvent__mutmut_42, 
        'xǁIconButtonǁpaintEvent__mutmut_43': xǁIconButtonǁpaintEvent__mutmut_43, 
        'xǁIconButtonǁpaintEvent__mutmut_44': xǁIconButtonǁpaintEvent__mutmut_44, 
        'xǁIconButtonǁpaintEvent__mutmut_45': xǁIconButtonǁpaintEvent__mutmut_45, 
        'xǁIconButtonǁpaintEvent__mutmut_46': xǁIconButtonǁpaintEvent__mutmut_46, 
        'xǁIconButtonǁpaintEvent__mutmut_47': xǁIconButtonǁpaintEvent__mutmut_47, 
        'xǁIconButtonǁpaintEvent__mutmut_48': xǁIconButtonǁpaintEvent__mutmut_48, 
        'xǁIconButtonǁpaintEvent__mutmut_49': xǁIconButtonǁpaintEvent__mutmut_49, 
        'xǁIconButtonǁpaintEvent__mutmut_50': xǁIconButtonǁpaintEvent__mutmut_50, 
        'xǁIconButtonǁpaintEvent__mutmut_51': xǁIconButtonǁpaintEvent__mutmut_51, 
        'xǁIconButtonǁpaintEvent__mutmut_52': xǁIconButtonǁpaintEvent__mutmut_52, 
        'xǁIconButtonǁpaintEvent__mutmut_53': xǁIconButtonǁpaintEvent__mutmut_53, 
        'xǁIconButtonǁpaintEvent__mutmut_54': xǁIconButtonǁpaintEvent__mutmut_54, 
        'xǁIconButtonǁpaintEvent__mutmut_55': xǁIconButtonǁpaintEvent__mutmut_55, 
        'xǁIconButtonǁpaintEvent__mutmut_56': xǁIconButtonǁpaintEvent__mutmut_56, 
        'xǁIconButtonǁpaintEvent__mutmut_57': xǁIconButtonǁpaintEvent__mutmut_57, 
        'xǁIconButtonǁpaintEvent__mutmut_58': xǁIconButtonǁpaintEvent__mutmut_58, 
        'xǁIconButtonǁpaintEvent__mutmut_59': xǁIconButtonǁpaintEvent__mutmut_59, 
        'xǁIconButtonǁpaintEvent__mutmut_60': xǁIconButtonǁpaintEvent__mutmut_60, 
        'xǁIconButtonǁpaintEvent__mutmut_61': xǁIconButtonǁpaintEvent__mutmut_61, 
        'xǁIconButtonǁpaintEvent__mutmut_62': xǁIconButtonǁpaintEvent__mutmut_62, 
        'xǁIconButtonǁpaintEvent__mutmut_63': xǁIconButtonǁpaintEvent__mutmut_63, 
        'xǁIconButtonǁpaintEvent__mutmut_64': xǁIconButtonǁpaintEvent__mutmut_64, 
        'xǁIconButtonǁpaintEvent__mutmut_65': xǁIconButtonǁpaintEvent__mutmut_65, 
        'xǁIconButtonǁpaintEvent__mutmut_66': xǁIconButtonǁpaintEvent__mutmut_66, 
        'xǁIconButtonǁpaintEvent__mutmut_67': xǁIconButtonǁpaintEvent__mutmut_67, 
        'xǁIconButtonǁpaintEvent__mutmut_68': xǁIconButtonǁpaintEvent__mutmut_68, 
        'xǁIconButtonǁpaintEvent__mutmut_69': xǁIconButtonǁpaintEvent__mutmut_69, 
        'xǁIconButtonǁpaintEvent__mutmut_70': xǁIconButtonǁpaintEvent__mutmut_70, 
        'xǁIconButtonǁpaintEvent__mutmut_71': xǁIconButtonǁpaintEvent__mutmut_71, 
        'xǁIconButtonǁpaintEvent__mutmut_72': xǁIconButtonǁpaintEvent__mutmut_72, 
        'xǁIconButtonǁpaintEvent__mutmut_73': xǁIconButtonǁpaintEvent__mutmut_73, 
        'xǁIconButtonǁpaintEvent__mutmut_74': xǁIconButtonǁpaintEvent__mutmut_74, 
        'xǁIconButtonǁpaintEvent__mutmut_75': xǁIconButtonǁpaintEvent__mutmut_75, 
        'xǁIconButtonǁpaintEvent__mutmut_76': xǁIconButtonǁpaintEvent__mutmut_76, 
        'xǁIconButtonǁpaintEvent__mutmut_77': xǁIconButtonǁpaintEvent__mutmut_77, 
        'xǁIconButtonǁpaintEvent__mutmut_78': xǁIconButtonǁpaintEvent__mutmut_78, 
        'xǁIconButtonǁpaintEvent__mutmut_79': xǁIconButtonǁpaintEvent__mutmut_79, 
        'xǁIconButtonǁpaintEvent__mutmut_80': xǁIconButtonǁpaintEvent__mutmut_80, 
        'xǁIconButtonǁpaintEvent__mutmut_81': xǁIconButtonǁpaintEvent__mutmut_81, 
        'xǁIconButtonǁpaintEvent__mutmut_82': xǁIconButtonǁpaintEvent__mutmut_82, 
        'xǁIconButtonǁpaintEvent__mutmut_83': xǁIconButtonǁpaintEvent__mutmut_83, 
        'xǁIconButtonǁpaintEvent__mutmut_84': xǁIconButtonǁpaintEvent__mutmut_84, 
        'xǁIconButtonǁpaintEvent__mutmut_85': xǁIconButtonǁpaintEvent__mutmut_85, 
        'xǁIconButtonǁpaintEvent__mutmut_86': xǁIconButtonǁpaintEvent__mutmut_86, 
        'xǁIconButtonǁpaintEvent__mutmut_87': xǁIconButtonǁpaintEvent__mutmut_87, 
        'xǁIconButtonǁpaintEvent__mutmut_88': xǁIconButtonǁpaintEvent__mutmut_88, 
        'xǁIconButtonǁpaintEvent__mutmut_89': xǁIconButtonǁpaintEvent__mutmut_89, 
        'xǁIconButtonǁpaintEvent__mutmut_90': xǁIconButtonǁpaintEvent__mutmut_90, 
        'xǁIconButtonǁpaintEvent__mutmut_91': xǁIconButtonǁpaintEvent__mutmut_91, 
        'xǁIconButtonǁpaintEvent__mutmut_92': xǁIconButtonǁpaintEvent__mutmut_92, 
        'xǁIconButtonǁpaintEvent__mutmut_93': xǁIconButtonǁpaintEvent__mutmut_93, 
        'xǁIconButtonǁpaintEvent__mutmut_94': xǁIconButtonǁpaintEvent__mutmut_94, 
        'xǁIconButtonǁpaintEvent__mutmut_95': xǁIconButtonǁpaintEvent__mutmut_95, 
        'xǁIconButtonǁpaintEvent__mutmut_96': xǁIconButtonǁpaintEvent__mutmut_96, 
        'xǁIconButtonǁpaintEvent__mutmut_97': xǁIconButtonǁpaintEvent__mutmut_97, 
        'xǁIconButtonǁpaintEvent__mutmut_98': xǁIconButtonǁpaintEvent__mutmut_98, 
        'xǁIconButtonǁpaintEvent__mutmut_99': xǁIconButtonǁpaintEvent__mutmut_99, 
        'xǁIconButtonǁpaintEvent__mutmut_100': xǁIconButtonǁpaintEvent__mutmut_100, 
        'xǁIconButtonǁpaintEvent__mutmut_101': xǁIconButtonǁpaintEvent__mutmut_101, 
        'xǁIconButtonǁpaintEvent__mutmut_102': xǁIconButtonǁpaintEvent__mutmut_102, 
        'xǁIconButtonǁpaintEvent__mutmut_103': xǁIconButtonǁpaintEvent__mutmut_103, 
        'xǁIconButtonǁpaintEvent__mutmut_104': xǁIconButtonǁpaintEvent__mutmut_104, 
        'xǁIconButtonǁpaintEvent__mutmut_105': xǁIconButtonǁpaintEvent__mutmut_105, 
        'xǁIconButtonǁpaintEvent__mutmut_106': xǁIconButtonǁpaintEvent__mutmut_106, 
        'xǁIconButtonǁpaintEvent__mutmut_107': xǁIconButtonǁpaintEvent__mutmut_107, 
        'xǁIconButtonǁpaintEvent__mutmut_108': xǁIconButtonǁpaintEvent__mutmut_108, 
        'xǁIconButtonǁpaintEvent__mutmut_109': xǁIconButtonǁpaintEvent__mutmut_109, 
        'xǁIconButtonǁpaintEvent__mutmut_110': xǁIconButtonǁpaintEvent__mutmut_110, 
        'xǁIconButtonǁpaintEvent__mutmut_111': xǁIconButtonǁpaintEvent__mutmut_111, 
        'xǁIconButtonǁpaintEvent__mutmut_112': xǁIconButtonǁpaintEvent__mutmut_112, 
        'xǁIconButtonǁpaintEvent__mutmut_113': xǁIconButtonǁpaintEvent__mutmut_113, 
        'xǁIconButtonǁpaintEvent__mutmut_114': xǁIconButtonǁpaintEvent__mutmut_114, 
        'xǁIconButtonǁpaintEvent__mutmut_115': xǁIconButtonǁpaintEvent__mutmut_115, 
        'xǁIconButtonǁpaintEvent__mutmut_116': xǁIconButtonǁpaintEvent__mutmut_116, 
        'xǁIconButtonǁpaintEvent__mutmut_117': xǁIconButtonǁpaintEvent__mutmut_117, 
        'xǁIconButtonǁpaintEvent__mutmut_118': xǁIconButtonǁpaintEvent__mutmut_118, 
        'xǁIconButtonǁpaintEvent__mutmut_119': xǁIconButtonǁpaintEvent__mutmut_119, 
        'xǁIconButtonǁpaintEvent__mutmut_120': xǁIconButtonǁpaintEvent__mutmut_120, 
        'xǁIconButtonǁpaintEvent__mutmut_121': xǁIconButtonǁpaintEvent__mutmut_121, 
        'xǁIconButtonǁpaintEvent__mutmut_122': xǁIconButtonǁpaintEvent__mutmut_122, 
        'xǁIconButtonǁpaintEvent__mutmut_123': xǁIconButtonǁpaintEvent__mutmut_123, 
        'xǁIconButtonǁpaintEvent__mutmut_124': xǁIconButtonǁpaintEvent__mutmut_124, 
        'xǁIconButtonǁpaintEvent__mutmut_125': xǁIconButtonǁpaintEvent__mutmut_125, 
        'xǁIconButtonǁpaintEvent__mutmut_126': xǁIconButtonǁpaintEvent__mutmut_126, 
        'xǁIconButtonǁpaintEvent__mutmut_127': xǁIconButtonǁpaintEvent__mutmut_127, 
        'xǁIconButtonǁpaintEvent__mutmut_128': xǁIconButtonǁpaintEvent__mutmut_128, 
        'xǁIconButtonǁpaintEvent__mutmut_129': xǁIconButtonǁpaintEvent__mutmut_129, 
        'xǁIconButtonǁpaintEvent__mutmut_130': xǁIconButtonǁpaintEvent__mutmut_130, 
        'xǁIconButtonǁpaintEvent__mutmut_131': xǁIconButtonǁpaintEvent__mutmut_131, 
        'xǁIconButtonǁpaintEvent__mutmut_132': xǁIconButtonǁpaintEvent__mutmut_132, 
        'xǁIconButtonǁpaintEvent__mutmut_133': xǁIconButtonǁpaintEvent__mutmut_133, 
        'xǁIconButtonǁpaintEvent__mutmut_134': xǁIconButtonǁpaintEvent__mutmut_134, 
        'xǁIconButtonǁpaintEvent__mutmut_135': xǁIconButtonǁpaintEvent__mutmut_135, 
        'xǁIconButtonǁpaintEvent__mutmut_136': xǁIconButtonǁpaintEvent__mutmut_136, 
        'xǁIconButtonǁpaintEvent__mutmut_137': xǁIconButtonǁpaintEvent__mutmut_137, 
        'xǁIconButtonǁpaintEvent__mutmut_138': xǁIconButtonǁpaintEvent__mutmut_138, 
        'xǁIconButtonǁpaintEvent__mutmut_139': xǁIconButtonǁpaintEvent__mutmut_139, 
        'xǁIconButtonǁpaintEvent__mutmut_140': xǁIconButtonǁpaintEvent__mutmut_140, 
        'xǁIconButtonǁpaintEvent__mutmut_141': xǁIconButtonǁpaintEvent__mutmut_141, 
        'xǁIconButtonǁpaintEvent__mutmut_142': xǁIconButtonǁpaintEvent__mutmut_142, 
        'xǁIconButtonǁpaintEvent__mutmut_143': xǁIconButtonǁpaintEvent__mutmut_143, 
        'xǁIconButtonǁpaintEvent__mutmut_144': xǁIconButtonǁpaintEvent__mutmut_144, 
        'xǁIconButtonǁpaintEvent__mutmut_145': xǁIconButtonǁpaintEvent__mutmut_145, 
        'xǁIconButtonǁpaintEvent__mutmut_146': xǁIconButtonǁpaintEvent__mutmut_146, 
        'xǁIconButtonǁpaintEvent__mutmut_147': xǁIconButtonǁpaintEvent__mutmut_147, 
        'xǁIconButtonǁpaintEvent__mutmut_148': xǁIconButtonǁpaintEvent__mutmut_148, 
        'xǁIconButtonǁpaintEvent__mutmut_149': xǁIconButtonǁpaintEvent__mutmut_149
    }
    xǁIconButtonǁpaintEvent__mutmut_orig.__name__ = 'xǁIconButtonǁpaintEvent'

    def setProperty(self, name: str, value: typing.Any) -> bool:
        args = [name, value]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁIconButtonǁsetProperty__mutmut_orig'), object.__getattribute__(self, 'xǁIconButtonǁsetProperty__mutmut_mutants'), args, kwargs, self)

    def xǁIconButtonǁsetProperty__mutmut_orig(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_1(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name != "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_2(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "XXicon_pixmapXX":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_3(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "ICON_PIXMAP":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_4(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = None
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_5(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name != "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_6(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "XXtext_formattingXX":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_7(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "TEXT_FORMATTING":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_8(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = None
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_9(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name != "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_10(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "XXhas_textXX":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_11(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "HAS_TEXT":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_12(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = None
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_13(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name != "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_14(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "XXnameXX":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_15(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "NAME":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_16(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = None
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_17(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name != "text_color":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_18(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "XXtext_colorXX":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_19(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "TEXT_COLOR":
            self.text_color = value
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_20(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = None
        return super().setProperty(name, value)

    def xǁIconButtonǁsetProperty__mutmut_21(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(None, value)

    def xǁIconButtonǁsetProperty__mutmut_22(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, None)

    def xǁIconButtonǁsetProperty__mutmut_23(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(value)

    def xǁIconButtonǁsetProperty__mutmut_24(self, name: str, value: typing.Any) -> bool:
        """Re-implemented method, set widget properties"""
        if name == "icon_pixmap":
            self.icon_pixmap = value
        elif name == "text_formatting":
            self.text_formatting = value
        elif name == "has_text":
            self.has_text = value
        elif name == "name":
            self._name = name
        elif name == "text_color":
            self.text_color = value
        return super().setProperty(name, )
    
    xǁIconButtonǁsetProperty__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁIconButtonǁsetProperty__mutmut_1': xǁIconButtonǁsetProperty__mutmut_1, 
        'xǁIconButtonǁsetProperty__mutmut_2': xǁIconButtonǁsetProperty__mutmut_2, 
        'xǁIconButtonǁsetProperty__mutmut_3': xǁIconButtonǁsetProperty__mutmut_3, 
        'xǁIconButtonǁsetProperty__mutmut_4': xǁIconButtonǁsetProperty__mutmut_4, 
        'xǁIconButtonǁsetProperty__mutmut_5': xǁIconButtonǁsetProperty__mutmut_5, 
        'xǁIconButtonǁsetProperty__mutmut_6': xǁIconButtonǁsetProperty__mutmut_6, 
        'xǁIconButtonǁsetProperty__mutmut_7': xǁIconButtonǁsetProperty__mutmut_7, 
        'xǁIconButtonǁsetProperty__mutmut_8': xǁIconButtonǁsetProperty__mutmut_8, 
        'xǁIconButtonǁsetProperty__mutmut_9': xǁIconButtonǁsetProperty__mutmut_9, 
        'xǁIconButtonǁsetProperty__mutmut_10': xǁIconButtonǁsetProperty__mutmut_10, 
        'xǁIconButtonǁsetProperty__mutmut_11': xǁIconButtonǁsetProperty__mutmut_11, 
        'xǁIconButtonǁsetProperty__mutmut_12': xǁIconButtonǁsetProperty__mutmut_12, 
        'xǁIconButtonǁsetProperty__mutmut_13': xǁIconButtonǁsetProperty__mutmut_13, 
        'xǁIconButtonǁsetProperty__mutmut_14': xǁIconButtonǁsetProperty__mutmut_14, 
        'xǁIconButtonǁsetProperty__mutmut_15': xǁIconButtonǁsetProperty__mutmut_15, 
        'xǁIconButtonǁsetProperty__mutmut_16': xǁIconButtonǁsetProperty__mutmut_16, 
        'xǁIconButtonǁsetProperty__mutmut_17': xǁIconButtonǁsetProperty__mutmut_17, 
        'xǁIconButtonǁsetProperty__mutmut_18': xǁIconButtonǁsetProperty__mutmut_18, 
        'xǁIconButtonǁsetProperty__mutmut_19': xǁIconButtonǁsetProperty__mutmut_19, 
        'xǁIconButtonǁsetProperty__mutmut_20': xǁIconButtonǁsetProperty__mutmut_20, 
        'xǁIconButtonǁsetProperty__mutmut_21': xǁIconButtonǁsetProperty__mutmut_21, 
        'xǁIconButtonǁsetProperty__mutmut_22': xǁIconButtonǁsetProperty__mutmut_22, 
        'xǁIconButtonǁsetProperty__mutmut_23': xǁIconButtonǁsetProperty__mutmut_23, 
        'xǁIconButtonǁsetProperty__mutmut_24': xǁIconButtonǁsetProperty__mutmut_24
    }
    xǁIconButtonǁsetProperty__mutmut_orig.__name__ = 'xǁIconButtonǁsetProperty'
