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


class BasePopup(QtWidgets.QDialog):
    """Simple  popup with custom message and Confirm/Back buttons

    To assert if the user accepted or rejected the dialog connect to the **accepted()** or **rejected()** signals.

    The `finished()` signal can also be used to get the result of the dialog. This is emitted after
    the accepted and rejected signals.


    """

    x_offset: float = 0.7
    y_offset: float = 0.7
    border_radius: int = 20
    border_margin: int = 5

    def __init__(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        args = [parent, floating, dialog]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁ__init____mutmut_orig(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_1(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = True,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_2(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_3(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(None)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_4(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            None
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_5(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint & QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_6(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog & QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_7(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = None
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_8(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = None
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_9(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = None
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_10(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "XX#ffffffXX"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_11(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#FFFFFF"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_12(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = None
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_13(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "XX#F44336XX"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_14(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#f44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_15(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = None
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_16(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "XX#4CAF50XX"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_17(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4caf50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_18(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = None
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_19(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "XX#ffffffXX"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_20(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#FFFFFF"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_21(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = None

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_22(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "XX#ffffffXX"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_23(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#FFFFFF"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_24(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(None, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_25(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, None)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_26(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_27(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, )
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_28(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, False)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_29(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(None)
        else:
            self.setStyleSheet(
                """
                #MyParent {
                    background-image: url(:/background/media/1st_background.png);
                }
            """
            )

    def xǁBasePopupǁ__init____mutmut_30(
        self,
        parent: QtWidgets.QWidget,  # Make parent optional for easier testing
        floating: bool = False,
        dialog: bool = True,
    ) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Dialog
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.CustomizeWindowHint
        )
        self.floating = floating
        self.dialog = dialog
        # Color Variables
        self.btns_text_color = "#ffffff"
        self.cancel_bk_color = "#F44336"
        self.confirm_bk_color = "#4CAF50"
        self.confirm_ft_color = "#ffffff"
        self.cancel_ft_color = "#ffffff"

        self.setupUI()
        self.update()

        if floating:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        else:
            self.setStyleSheet(
                None
            )
    
    xǁBasePopupǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁ__init____mutmut_1': xǁBasePopupǁ__init____mutmut_1, 
        'xǁBasePopupǁ__init____mutmut_2': xǁBasePopupǁ__init____mutmut_2, 
        'xǁBasePopupǁ__init____mutmut_3': xǁBasePopupǁ__init____mutmut_3, 
        'xǁBasePopupǁ__init____mutmut_4': xǁBasePopupǁ__init____mutmut_4, 
        'xǁBasePopupǁ__init____mutmut_5': xǁBasePopupǁ__init____mutmut_5, 
        'xǁBasePopupǁ__init____mutmut_6': xǁBasePopupǁ__init____mutmut_6, 
        'xǁBasePopupǁ__init____mutmut_7': xǁBasePopupǁ__init____mutmut_7, 
        'xǁBasePopupǁ__init____mutmut_8': xǁBasePopupǁ__init____mutmut_8, 
        'xǁBasePopupǁ__init____mutmut_9': xǁBasePopupǁ__init____mutmut_9, 
        'xǁBasePopupǁ__init____mutmut_10': xǁBasePopupǁ__init____mutmut_10, 
        'xǁBasePopupǁ__init____mutmut_11': xǁBasePopupǁ__init____mutmut_11, 
        'xǁBasePopupǁ__init____mutmut_12': xǁBasePopupǁ__init____mutmut_12, 
        'xǁBasePopupǁ__init____mutmut_13': xǁBasePopupǁ__init____mutmut_13, 
        'xǁBasePopupǁ__init____mutmut_14': xǁBasePopupǁ__init____mutmut_14, 
        'xǁBasePopupǁ__init____mutmut_15': xǁBasePopupǁ__init____mutmut_15, 
        'xǁBasePopupǁ__init____mutmut_16': xǁBasePopupǁ__init____mutmut_16, 
        'xǁBasePopupǁ__init____mutmut_17': xǁBasePopupǁ__init____mutmut_17, 
        'xǁBasePopupǁ__init____mutmut_18': xǁBasePopupǁ__init____mutmut_18, 
        'xǁBasePopupǁ__init____mutmut_19': xǁBasePopupǁ__init____mutmut_19, 
        'xǁBasePopupǁ__init____mutmut_20': xǁBasePopupǁ__init____mutmut_20, 
        'xǁBasePopupǁ__init____mutmut_21': xǁBasePopupǁ__init____mutmut_21, 
        'xǁBasePopupǁ__init____mutmut_22': xǁBasePopupǁ__init____mutmut_22, 
        'xǁBasePopupǁ__init____mutmut_23': xǁBasePopupǁ__init____mutmut_23, 
        'xǁBasePopupǁ__init____mutmut_24': xǁBasePopupǁ__init____mutmut_24, 
        'xǁBasePopupǁ__init____mutmut_25': xǁBasePopupǁ__init____mutmut_25, 
        'xǁBasePopupǁ__init____mutmut_26': xǁBasePopupǁ__init____mutmut_26, 
        'xǁBasePopupǁ__init____mutmut_27': xǁBasePopupǁ__init____mutmut_27, 
        'xǁBasePopupǁ__init____mutmut_28': xǁBasePopupǁ__init____mutmut_28, 
        'xǁBasePopupǁ__init____mutmut_29': xǁBasePopupǁ__init____mutmut_29, 
        'xǁBasePopupǁ__init____mutmut_30': xǁBasePopupǁ__init____mutmut_30
    }
    xǁBasePopupǁ__init____mutmut_orig.__name__ = 'xǁBasePopupǁ__init__'

    def _update_button_style(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁ_update_button_style__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁ_update_button_style__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁ_update_button_style__mutmut_orig(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if not self.dialog:
            return

        if not self.floating:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border: none;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border: none;
                padding: 10px;
                """
            )
        else:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border-top: none; 
                border-left: 2px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 1px solid #80807e; 
                border-bottom-left-radius: 16px;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border-left: 1px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 2px solid #80807e; 
                border-bottom-right-radius: 16px;
                padding: 10px;
                """
            )

    def xǁBasePopupǁ_update_button_style__mutmut_1(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if self.dialog:
            return

        if not self.floating:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border: none;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border: none;
                padding: 10px;
                """
            )
        else:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border-top: none; 
                border-left: 2px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 1px solid #80807e; 
                border-bottom-left-radius: 16px;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border-left: 1px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 2px solid #80807e; 
                border-bottom-right-radius: 16px;
                padding: 10px;
                """
            )

    def xǁBasePopupǁ_update_button_style__mutmut_2(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if not self.dialog:
            return

        if self.floating:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border: none;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border: none;
                padding: 10px;
                """
            )
        else:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border-top: none; 
                border-left: 2px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 1px solid #80807e; 
                border-bottom-left-radius: 16px;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border-left: 1px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 2px solid #80807e; 
                border-bottom-right-radius: 16px;
                padding: 10px;
                """
            )

    def xǁBasePopupǁ_update_button_style__mutmut_3(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if not self.dialog:
            return

        if not self.floating:
            self.confirm_button.setStyleSheet(
                None
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border: none;
                padding: 10px;
                """
            )
        else:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border-top: none; 
                border-left: 2px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 1px solid #80807e; 
                border-bottom-left-radius: 16px;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border-left: 1px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 2px solid #80807e; 
                border-bottom-right-radius: 16px;
                padding: 10px;
                """
            )

    def xǁBasePopupǁ_update_button_style__mutmut_4(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if not self.dialog:
            return

        if not self.floating:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border: none;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                None
            )
        else:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border-top: none; 
                border-left: 2px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 1px solid #80807e; 
                border-bottom-left-radius: 16px;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border-left: 1px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 2px solid #80807e; 
                border-bottom-right-radius: 16px;
                padding: 10px;
                """
            )

    def xǁBasePopupǁ_update_button_style__mutmut_5(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if not self.dialog:
            return

        if not self.floating:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border: none;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border: none;
                padding: 10px;
                """
            )
        else:
            self.confirm_button.setStyleSheet(
                None
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border-left: 1px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 2px solid #80807e; 
                border-bottom-right-radius: 16px;
                padding: 10px;
                """
            )

    def xǁBasePopupǁ_update_button_style__mutmut_6(self) -> None:
        """Applies the current color variables and adds the central border to the stylesheets."""
        if not self.dialog:
            return

        if not self.floating:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border: none;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                f"""
                background-color: {self.cancel_bk_color};
                color: {self.cancel_ft_color};
                border: none;
                padding: 10px;
                """
            )
        else:
            self.confirm_button.setStyleSheet(
                f"""
                background-color: {self.confirm_bk_color};
                color: {self.confirm_ft_color};
                border-top: none; 
                border-left: 2px solid #80807e;; 
                border-bottom: 2px solid #80807e;
                border-right: 1px solid #80807e; 
                border-bottom-left-radius: 16px;
                padding: 10px;
                """
            )

            self.cancel_button.setStyleSheet(
                None
            )
    
    xǁBasePopupǁ_update_button_style__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁ_update_button_style__mutmut_1': xǁBasePopupǁ_update_button_style__mutmut_1, 
        'xǁBasePopupǁ_update_button_style__mutmut_2': xǁBasePopupǁ_update_button_style__mutmut_2, 
        'xǁBasePopupǁ_update_button_style__mutmut_3': xǁBasePopupǁ_update_button_style__mutmut_3, 
        'xǁBasePopupǁ_update_button_style__mutmut_4': xǁBasePopupǁ_update_button_style__mutmut_4, 
        'xǁBasePopupǁ_update_button_style__mutmut_5': xǁBasePopupǁ_update_button_style__mutmut_5, 
        'xǁBasePopupǁ_update_button_style__mutmut_6': xǁBasePopupǁ_update_button_style__mutmut_6
    }
    xǁBasePopupǁ_update_button_style__mutmut_orig.__name__ = 'xǁBasePopupǁ_update_button_style'

    def set_message(self, message: str) -> None:
        args = [message]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁset_message__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁset_message__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁset_message__mutmut_orig(self, message: str) -> None:
        self.label.setText(message)

    def xǁBasePopupǁset_message__mutmut_1(self, message: str) -> None:
        self.label.setText(None)
    
    xǁBasePopupǁset_message__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁset_message__mutmut_1': xǁBasePopupǁset_message__mutmut_1
    }
    xǁBasePopupǁset_message__mutmut_orig.__name__ = 'xǁBasePopupǁset_message'

    def cancel_button_text(self, text: str) -> None:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁcancel_button_text__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁcancel_button_text__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁcancel_button_text__mutmut_orig(self, text: str) -> None:
        if not self.dialog:
            return
        self.cancel_button.setText(text)

    def xǁBasePopupǁcancel_button_text__mutmut_1(self, text: str) -> None:
        if self.dialog:
            return
        self.cancel_button.setText(text)

    def xǁBasePopupǁcancel_button_text__mutmut_2(self, text: str) -> None:
        if not self.dialog:
            return
        self.cancel_button.setText(None)
    
    xǁBasePopupǁcancel_button_text__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁcancel_button_text__mutmut_1': xǁBasePopupǁcancel_button_text__mutmut_1, 
        'xǁBasePopupǁcancel_button_text__mutmut_2': xǁBasePopupǁcancel_button_text__mutmut_2
    }
    xǁBasePopupǁcancel_button_text__mutmut_orig.__name__ = 'xǁBasePopupǁcancel_button_text'

    def confirm_button_text(self, text: str) -> None:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁconfirm_button_text__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁconfirm_button_text__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁconfirm_button_text__mutmut_orig(self, text: str) -> None:
        if not self.dialog:
            return
        self.confirm_button.setText(text)

    def xǁBasePopupǁconfirm_button_text__mutmut_1(self, text: str) -> None:
        if self.dialog:
            return
        self.confirm_button.setText(text)

    def xǁBasePopupǁconfirm_button_text__mutmut_2(self, text: str) -> None:
        if not self.dialog:
            return
        self.confirm_button.setText(None)
    
    xǁBasePopupǁconfirm_button_text__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁconfirm_button_text__mutmut_1': xǁBasePopupǁconfirm_button_text__mutmut_1, 
        'xǁBasePopupǁconfirm_button_text__mutmut_2': xǁBasePopupǁconfirm_button_text__mutmut_2
    }
    xǁBasePopupǁconfirm_button_text__mutmut_orig.__name__ = 'xǁBasePopupǁconfirm_button_text'

    def cancel_background_color(self, color: str) -> None:
        args = [color]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁcancel_background_color__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁcancel_background_color__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁcancel_background_color__mutmut_orig(self, color: str) -> None:
        if not self.dialog:
            return
        self.cancel_bk_color = color
        self._update_button_style()

    def xǁBasePopupǁcancel_background_color__mutmut_1(self, color: str) -> None:
        if self.dialog:
            return
        self.cancel_bk_color = color
        self._update_button_style()

    def xǁBasePopupǁcancel_background_color__mutmut_2(self, color: str) -> None:
        if not self.dialog:
            return
        self.cancel_bk_color = None
        self._update_button_style()
    
    xǁBasePopupǁcancel_background_color__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁcancel_background_color__mutmut_1': xǁBasePopupǁcancel_background_color__mutmut_1, 
        'xǁBasePopupǁcancel_background_color__mutmut_2': xǁBasePopupǁcancel_background_color__mutmut_2
    }
    xǁBasePopupǁcancel_background_color__mutmut_orig.__name__ = 'xǁBasePopupǁcancel_background_color'

    def confirm_background_color(self, color: str) -> None:
        args = [color]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁconfirm_background_color__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁconfirm_background_color__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁconfirm_background_color__mutmut_orig(self, color: str) -> None:
        if not self.dialog:
            return
        self.confirm_bk_color = color
        self._update_button_style()

    def xǁBasePopupǁconfirm_background_color__mutmut_1(self, color: str) -> None:
        if self.dialog:
            return
        self.confirm_bk_color = color
        self._update_button_style()

    def xǁBasePopupǁconfirm_background_color__mutmut_2(self, color: str) -> None:
        if not self.dialog:
            return
        self.confirm_bk_color = None
        self._update_button_style()
    
    xǁBasePopupǁconfirm_background_color__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁconfirm_background_color__mutmut_1': xǁBasePopupǁconfirm_background_color__mutmut_1, 
        'xǁBasePopupǁconfirm_background_color__mutmut_2': xǁBasePopupǁconfirm_background_color__mutmut_2
    }
    xǁBasePopupǁconfirm_background_color__mutmut_orig.__name__ = 'xǁBasePopupǁconfirm_background_color'

    def cancel_font_color(self, color: str) -> None:
        args = [color]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁcancel_font_color__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁcancel_font_color__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁcancel_font_color__mutmut_orig(self, color: str) -> None:
        if not self.dialog:
            return
        self.cancel_ft_color = color
        self._update_button_style()

    def xǁBasePopupǁcancel_font_color__mutmut_1(self, color: str) -> None:
        if self.dialog:
            return
        self.cancel_ft_color = color
        self._update_button_style()

    def xǁBasePopupǁcancel_font_color__mutmut_2(self, color: str) -> None:
        if not self.dialog:
            return
        self.cancel_ft_color = None
        self._update_button_style()
    
    xǁBasePopupǁcancel_font_color__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁcancel_font_color__mutmut_1': xǁBasePopupǁcancel_font_color__mutmut_1, 
        'xǁBasePopupǁcancel_font_color__mutmut_2': xǁBasePopupǁcancel_font_color__mutmut_2
    }
    xǁBasePopupǁcancel_font_color__mutmut_orig.__name__ = 'xǁBasePopupǁcancel_font_color'

    def confirm_font_color(self, color: str) -> None:
        args = [color]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁconfirm_font_color__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁconfirm_font_color__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁconfirm_font_color__mutmut_orig(self, color: str) -> None:
        if not self.dialog:
            return
        self.confirm_ft_color = color
        self._update_button_style()

    def xǁBasePopupǁconfirm_font_color__mutmut_1(self, color: str) -> None:
        if self.dialog:
            return
        self.confirm_ft_color = color
        self._update_button_style()

    def xǁBasePopupǁconfirm_font_color__mutmut_2(self, color: str) -> None:
        if not self.dialog:
            return
        self.confirm_ft_color = None
        self._update_button_style()
    
    xǁBasePopupǁconfirm_font_color__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁconfirm_font_color__mutmut_1': xǁBasePopupǁconfirm_font_color__mutmut_1, 
        'xǁBasePopupǁconfirm_font_color__mutmut_2': xǁBasePopupǁconfirm_font_color__mutmut_2
    }
    xǁBasePopupǁconfirm_font_color__mutmut_orig.__name__ = 'xǁBasePopupǁconfirm_font_color'

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        args = [widget]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁadd_widget__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁadd_widget__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁadd_widget__mutmut_orig(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = self.vlayout
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, self.ui)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_1(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = None
        layout = self.vlayout
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, self.ui)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_2(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = None
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, self.ui)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_3(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = self.vlayout
        index = None
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, self.ui)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_4(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = self.vlayout
        index = layout.indexOf(None)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, self.ui)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_5(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = self.vlayout
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(None, self.ui)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_6(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = self.vlayout
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, None)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_7(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = self.vlayout
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(self.ui)
        self.ui.show()

    def xǁBasePopupǁadd_widget__mutmut_8(self, widget: QtWidgets.QWidget) -> None:
        """Replace the label with a custom widget in the layout"""

        self.ui = widget
        layout = self.vlayout
        index = layout.indexOf(self.label)
        self.label.setParent(None)
        self.label.hide()
        layout.insertWidget(index, )
        self.ui.show()
    
    xǁBasePopupǁadd_widget__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁadd_widget__mutmut_1': xǁBasePopupǁadd_widget__mutmut_1, 
        'xǁBasePopupǁadd_widget__mutmut_2': xǁBasePopupǁadd_widget__mutmut_2, 
        'xǁBasePopupǁadd_widget__mutmut_3': xǁBasePopupǁadd_widget__mutmut_3, 
        'xǁBasePopupǁadd_widget__mutmut_4': xǁBasePopupǁadd_widget__mutmut_4, 
        'xǁBasePopupǁadd_widget__mutmut_5': xǁBasePopupǁadd_widget__mutmut_5, 
        'xǁBasePopupǁadd_widget__mutmut_6': xǁBasePopupǁadd_widget__mutmut_6, 
        'xǁBasePopupǁadd_widget__mutmut_7': xǁBasePopupǁadd_widget__mutmut_7, 
        'xǁBasePopupǁadd_widget__mutmut_8': xǁBasePopupǁadd_widget__mutmut_8
    }
    xǁBasePopupǁadd_widget__mutmut_orig.__name__ = 'xǁBasePopupǁadd_widget'

    def _get_mainWindow_widget(self) -> typing.Optional[QtWidgets.QMainWindow]:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁ_get_mainWindow_widget__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁ_get_mainWindow_widget__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁ_get_mainWindow_widget__mutmut_orig(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = QtWidgets.QApplication.instance()
        if not app_instance:
            return None
        main_window = app_instance.activeWindow()
        if main_window is None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None

    def xǁBasePopupǁ_get_mainWindow_widget__mutmut_1(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = None
        if not app_instance:
            return None
        main_window = app_instance.activeWindow()
        if main_window is None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None

    def xǁBasePopupǁ_get_mainWindow_widget__mutmut_2(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = QtWidgets.QApplication.instance()
        if app_instance:
            return None
        main_window = app_instance.activeWindow()
        if main_window is None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None

    def xǁBasePopupǁ_get_mainWindow_widget__mutmut_3(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = QtWidgets.QApplication.instance()
        if not app_instance:
            return None
        main_window = None
        if main_window is None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None

    def xǁBasePopupǁ_get_mainWindow_widget__mutmut_4(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = QtWidgets.QApplication.instance()
        if not app_instance:
            return None
        main_window = app_instance.activeWindow()
        if main_window is not None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    break
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None

    def xǁBasePopupǁ_get_mainWindow_widget__mutmut_5(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = QtWidgets.QApplication.instance()
        if not app_instance:
            return None
        main_window = app_instance.activeWindow()
        if main_window is None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = None
                    break
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None

    def xǁBasePopupǁ_get_mainWindow_widget__mutmut_6(self) -> typing.Optional[QtWidgets.QMainWindow]:
        """Get the main application window"""
        app_instance = QtWidgets.QApplication.instance()
        if not app_instance:
            return None
        main_window = app_instance.activeWindow()
        if main_window is None:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
                    return
        return main_window if isinstance(main_window, QtWidgets.QMainWindow) else None
    
    xǁBasePopupǁ_get_mainWindow_widget__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁ_get_mainWindow_widget__mutmut_1': xǁBasePopupǁ_get_mainWindow_widget__mutmut_1, 
        'xǁBasePopupǁ_get_mainWindow_widget__mutmut_2': xǁBasePopupǁ_get_mainWindow_widget__mutmut_2, 
        'xǁBasePopupǁ_get_mainWindow_widget__mutmut_3': xǁBasePopupǁ_get_mainWindow_widget__mutmut_3, 
        'xǁBasePopupǁ_get_mainWindow_widget__mutmut_4': xǁBasePopupǁ_get_mainWindow_widget__mutmut_4, 
        'xǁBasePopupǁ_get_mainWindow_widget__mutmut_5': xǁBasePopupǁ_get_mainWindow_widget__mutmut_5, 
        'xǁBasePopupǁ_get_mainWindow_widget__mutmut_6': xǁBasePopupǁ_get_mainWindow_widget__mutmut_6
    }
    xǁBasePopupǁ_get_mainWindow_widget__mutmut_orig.__name__ = 'xǁBasePopupǁ_get_mainWindow_widget'

    def _geometry_calc(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁ_geometry_calc__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁ_geometry_calc__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁ_geometry_calc__mutmut_orig(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_1(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = None
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_2(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is not None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_3(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = None
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_4(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(None)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_5(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() / self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_6(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = None
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_7(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(None)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_8(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() / self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_9(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = None
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_10(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(None)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_11(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() - (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_12(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) * 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_13(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() + width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_14(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 3)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_15(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = None
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_16(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(None)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_17(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() - (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_18(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) * 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_19(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() + height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_20(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 3)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_21(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = None
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_22(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = None
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_23(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = None
            height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_24(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = None

        self.setGeometry(x, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_25(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(None, y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_26(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, None, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_27(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, None, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_28(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, None)

    def xǁBasePopupǁ_geometry_calc__mutmut_29(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(y, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_30(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, width, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_31(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, height)

    def xǁBasePopupǁ_geometry_calc__mutmut_32(self) -> None:
        """Calculate dialog widget position relative to the window"""
        main_window = self._get_mainWindow_widget()
        if main_window is None:
            return

        if self.floating:
            width = int(main_window.width() * self.x_offset)
            height = int(main_window.height() * self.y_offset)
            x = int(main_window.geometry().x() + (main_window.width() - width) / 2)
            y = int(main_window.geometry().y() + (main_window.height() - height) / 2)
        else:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()

        self.setGeometry(x, y, width, )
    
    xǁBasePopupǁ_geometry_calc__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁ_geometry_calc__mutmut_1': xǁBasePopupǁ_geometry_calc__mutmut_1, 
        'xǁBasePopupǁ_geometry_calc__mutmut_2': xǁBasePopupǁ_geometry_calc__mutmut_2, 
        'xǁBasePopupǁ_geometry_calc__mutmut_3': xǁBasePopupǁ_geometry_calc__mutmut_3, 
        'xǁBasePopupǁ_geometry_calc__mutmut_4': xǁBasePopupǁ_geometry_calc__mutmut_4, 
        'xǁBasePopupǁ_geometry_calc__mutmut_5': xǁBasePopupǁ_geometry_calc__mutmut_5, 
        'xǁBasePopupǁ_geometry_calc__mutmut_6': xǁBasePopupǁ_geometry_calc__mutmut_6, 
        'xǁBasePopupǁ_geometry_calc__mutmut_7': xǁBasePopupǁ_geometry_calc__mutmut_7, 
        'xǁBasePopupǁ_geometry_calc__mutmut_8': xǁBasePopupǁ_geometry_calc__mutmut_8, 
        'xǁBasePopupǁ_geometry_calc__mutmut_9': xǁBasePopupǁ_geometry_calc__mutmut_9, 
        'xǁBasePopupǁ_geometry_calc__mutmut_10': xǁBasePopupǁ_geometry_calc__mutmut_10, 
        'xǁBasePopupǁ_geometry_calc__mutmut_11': xǁBasePopupǁ_geometry_calc__mutmut_11, 
        'xǁBasePopupǁ_geometry_calc__mutmut_12': xǁBasePopupǁ_geometry_calc__mutmut_12, 
        'xǁBasePopupǁ_geometry_calc__mutmut_13': xǁBasePopupǁ_geometry_calc__mutmut_13, 
        'xǁBasePopupǁ_geometry_calc__mutmut_14': xǁBasePopupǁ_geometry_calc__mutmut_14, 
        'xǁBasePopupǁ_geometry_calc__mutmut_15': xǁBasePopupǁ_geometry_calc__mutmut_15, 
        'xǁBasePopupǁ_geometry_calc__mutmut_16': xǁBasePopupǁ_geometry_calc__mutmut_16, 
        'xǁBasePopupǁ_geometry_calc__mutmut_17': xǁBasePopupǁ_geometry_calc__mutmut_17, 
        'xǁBasePopupǁ_geometry_calc__mutmut_18': xǁBasePopupǁ_geometry_calc__mutmut_18, 
        'xǁBasePopupǁ_geometry_calc__mutmut_19': xǁBasePopupǁ_geometry_calc__mutmut_19, 
        'xǁBasePopupǁ_geometry_calc__mutmut_20': xǁBasePopupǁ_geometry_calc__mutmut_20, 
        'xǁBasePopupǁ_geometry_calc__mutmut_21': xǁBasePopupǁ_geometry_calc__mutmut_21, 
        'xǁBasePopupǁ_geometry_calc__mutmut_22': xǁBasePopupǁ_geometry_calc__mutmut_22, 
        'xǁBasePopupǁ_geometry_calc__mutmut_23': xǁBasePopupǁ_geometry_calc__mutmut_23, 
        'xǁBasePopupǁ_geometry_calc__mutmut_24': xǁBasePopupǁ_geometry_calc__mutmut_24, 
        'xǁBasePopupǁ_geometry_calc__mutmut_25': xǁBasePopupǁ_geometry_calc__mutmut_25, 
        'xǁBasePopupǁ_geometry_calc__mutmut_26': xǁBasePopupǁ_geometry_calc__mutmut_26, 
        'xǁBasePopupǁ_geometry_calc__mutmut_27': xǁBasePopupǁ_geometry_calc__mutmut_27, 
        'xǁBasePopupǁ_geometry_calc__mutmut_28': xǁBasePopupǁ_geometry_calc__mutmut_28, 
        'xǁBasePopupǁ_geometry_calc__mutmut_29': xǁBasePopupǁ_geometry_calc__mutmut_29, 
        'xǁBasePopupǁ_geometry_calc__mutmut_30': xǁBasePopupǁ_geometry_calc__mutmut_30, 
        'xǁBasePopupǁ_geometry_calc__mutmut_31': xǁBasePopupǁ_geometry_calc__mutmut_31, 
        'xǁBasePopupǁ_geometry_calc__mutmut_32': xǁBasePopupǁ_geometry_calc__mutmut_32
    }
    xǁBasePopupǁ_geometry_calc__mutmut_orig.__name__ = 'xǁBasePopupǁ_geometry_calc'

    def sizeHint(self) -> QtCore.QSize:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁsizeHint__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁsizeHint__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁsizeHint__mutmut_orig(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_1(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = None
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_2(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(None)
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_3(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = None
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_4(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(None)
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_5(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = None
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_6(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = None
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_7(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() - (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_8(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) / 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_9(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() + popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_10(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 3
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_11(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(None, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_12(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, None)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_13(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_14(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, )
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_15(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(None, popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_16(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, None)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_17(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_height)
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_18(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, )
        self.setMinimumSize(popup_width, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_19(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(None, popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_20(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, None)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_21(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_height)
        return super().sizeHint()

    def xǁBasePopupǁsizeHint__mutmut_22(self) -> QtCore.QSize:
        """Re-implemented method, widget size hint"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, )
        return super().sizeHint()
    
    xǁBasePopupǁsizeHint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁsizeHint__mutmut_1': xǁBasePopupǁsizeHint__mutmut_1, 
        'xǁBasePopupǁsizeHint__mutmut_2': xǁBasePopupǁsizeHint__mutmut_2, 
        'xǁBasePopupǁsizeHint__mutmut_3': xǁBasePopupǁsizeHint__mutmut_3, 
        'xǁBasePopupǁsizeHint__mutmut_4': xǁBasePopupǁsizeHint__mutmut_4, 
        'xǁBasePopupǁsizeHint__mutmut_5': xǁBasePopupǁsizeHint__mutmut_5, 
        'xǁBasePopupǁsizeHint__mutmut_6': xǁBasePopupǁsizeHint__mutmut_6, 
        'xǁBasePopupǁsizeHint__mutmut_7': xǁBasePopupǁsizeHint__mutmut_7, 
        'xǁBasePopupǁsizeHint__mutmut_8': xǁBasePopupǁsizeHint__mutmut_8, 
        'xǁBasePopupǁsizeHint__mutmut_9': xǁBasePopupǁsizeHint__mutmut_9, 
        'xǁBasePopupǁsizeHint__mutmut_10': xǁBasePopupǁsizeHint__mutmut_10, 
        'xǁBasePopupǁsizeHint__mutmut_11': xǁBasePopupǁsizeHint__mutmut_11, 
        'xǁBasePopupǁsizeHint__mutmut_12': xǁBasePopupǁsizeHint__mutmut_12, 
        'xǁBasePopupǁsizeHint__mutmut_13': xǁBasePopupǁsizeHint__mutmut_13, 
        'xǁBasePopupǁsizeHint__mutmut_14': xǁBasePopupǁsizeHint__mutmut_14, 
        'xǁBasePopupǁsizeHint__mutmut_15': xǁBasePopupǁsizeHint__mutmut_15, 
        'xǁBasePopupǁsizeHint__mutmut_16': xǁBasePopupǁsizeHint__mutmut_16, 
        'xǁBasePopupǁsizeHint__mutmut_17': xǁBasePopupǁsizeHint__mutmut_17, 
        'xǁBasePopupǁsizeHint__mutmut_18': xǁBasePopupǁsizeHint__mutmut_18, 
        'xǁBasePopupǁsizeHint__mutmut_19': xǁBasePopupǁsizeHint__mutmut_19, 
        'xǁBasePopupǁsizeHint__mutmut_20': xǁBasePopupǁsizeHint__mutmut_20, 
        'xǁBasePopupǁsizeHint__mutmut_21': xǁBasePopupǁsizeHint__mutmut_21, 
        'xǁBasePopupǁsizeHint__mutmut_22': xǁBasePopupǁsizeHint__mutmut_22
    }
    xǁBasePopupǁsizeHint__mutmut_orig.__name__ = 'xǁBasePopupǁsizeHint'

    def open(self):
        """Re-implemented method, open widget"""
        self._geometry_calc()
        return super().open()

    def show(self) -> None:
        self._geometry_calc()
        return super().show()

    def paintEvent(self, a0: QtGui.QPaintEvent | None) -> None:
        args = [a0]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁpaintEvent__mutmut_orig(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_1(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_2(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_3(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_4(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_5(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, None)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_6(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_7(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, )
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_8(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, False)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_9(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = None
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_10(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(None)
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_11(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(None))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_12(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(None, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_13(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, None, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_14(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, None)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_15(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_16(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_17(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, )))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_18(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(64, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_19(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 64, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_20(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 64)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_21(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = None
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_22(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(None, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_23(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, None, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_24(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, None)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_25(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_26(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_27(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, )
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_28(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(129, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_29(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 129, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_30(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 129)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_31(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = None
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_32(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(None)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_33(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(None)
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_34(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(None, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_35(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, None))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_36(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_37(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, ))
        painter.drawRoundedRect(rect, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_38(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(None, self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_39(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, None, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_40(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, None)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_41(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(self.border_radius, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_42(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius)
        painter.end()

    def xǁBasePopupǁpaintEvent__mutmut_43(self, a0: QtGui.QPaintEvent | None) -> None:
        """Re-implemented method, paint widget"""
        if not self.floating:
            return

        self._geometry_calc()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 63, 63)))
        border_color = QtGui.QColor(128, 128, 128)
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(QtGui.QPen(border_color, self.border_margin))
        painter.drawRoundedRect(rect, self.border_radius, )
        painter.end()
    
    xǁBasePopupǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁpaintEvent__mutmut_1': xǁBasePopupǁpaintEvent__mutmut_1, 
        'xǁBasePopupǁpaintEvent__mutmut_2': xǁBasePopupǁpaintEvent__mutmut_2, 
        'xǁBasePopupǁpaintEvent__mutmut_3': xǁBasePopupǁpaintEvent__mutmut_3, 
        'xǁBasePopupǁpaintEvent__mutmut_4': xǁBasePopupǁpaintEvent__mutmut_4, 
        'xǁBasePopupǁpaintEvent__mutmut_5': xǁBasePopupǁpaintEvent__mutmut_5, 
        'xǁBasePopupǁpaintEvent__mutmut_6': xǁBasePopupǁpaintEvent__mutmut_6, 
        'xǁBasePopupǁpaintEvent__mutmut_7': xǁBasePopupǁpaintEvent__mutmut_7, 
        'xǁBasePopupǁpaintEvent__mutmut_8': xǁBasePopupǁpaintEvent__mutmut_8, 
        'xǁBasePopupǁpaintEvent__mutmut_9': xǁBasePopupǁpaintEvent__mutmut_9, 
        'xǁBasePopupǁpaintEvent__mutmut_10': xǁBasePopupǁpaintEvent__mutmut_10, 
        'xǁBasePopupǁpaintEvent__mutmut_11': xǁBasePopupǁpaintEvent__mutmut_11, 
        'xǁBasePopupǁpaintEvent__mutmut_12': xǁBasePopupǁpaintEvent__mutmut_12, 
        'xǁBasePopupǁpaintEvent__mutmut_13': xǁBasePopupǁpaintEvent__mutmut_13, 
        'xǁBasePopupǁpaintEvent__mutmut_14': xǁBasePopupǁpaintEvent__mutmut_14, 
        'xǁBasePopupǁpaintEvent__mutmut_15': xǁBasePopupǁpaintEvent__mutmut_15, 
        'xǁBasePopupǁpaintEvent__mutmut_16': xǁBasePopupǁpaintEvent__mutmut_16, 
        'xǁBasePopupǁpaintEvent__mutmut_17': xǁBasePopupǁpaintEvent__mutmut_17, 
        'xǁBasePopupǁpaintEvent__mutmut_18': xǁBasePopupǁpaintEvent__mutmut_18, 
        'xǁBasePopupǁpaintEvent__mutmut_19': xǁBasePopupǁpaintEvent__mutmut_19, 
        'xǁBasePopupǁpaintEvent__mutmut_20': xǁBasePopupǁpaintEvent__mutmut_20, 
        'xǁBasePopupǁpaintEvent__mutmut_21': xǁBasePopupǁpaintEvent__mutmut_21, 
        'xǁBasePopupǁpaintEvent__mutmut_22': xǁBasePopupǁpaintEvent__mutmut_22, 
        'xǁBasePopupǁpaintEvent__mutmut_23': xǁBasePopupǁpaintEvent__mutmut_23, 
        'xǁBasePopupǁpaintEvent__mutmut_24': xǁBasePopupǁpaintEvent__mutmut_24, 
        'xǁBasePopupǁpaintEvent__mutmut_25': xǁBasePopupǁpaintEvent__mutmut_25, 
        'xǁBasePopupǁpaintEvent__mutmut_26': xǁBasePopupǁpaintEvent__mutmut_26, 
        'xǁBasePopupǁpaintEvent__mutmut_27': xǁBasePopupǁpaintEvent__mutmut_27, 
        'xǁBasePopupǁpaintEvent__mutmut_28': xǁBasePopupǁpaintEvent__mutmut_28, 
        'xǁBasePopupǁpaintEvent__mutmut_29': xǁBasePopupǁpaintEvent__mutmut_29, 
        'xǁBasePopupǁpaintEvent__mutmut_30': xǁBasePopupǁpaintEvent__mutmut_30, 
        'xǁBasePopupǁpaintEvent__mutmut_31': xǁBasePopupǁpaintEvent__mutmut_31, 
        'xǁBasePopupǁpaintEvent__mutmut_32': xǁBasePopupǁpaintEvent__mutmut_32, 
        'xǁBasePopupǁpaintEvent__mutmut_33': xǁBasePopupǁpaintEvent__mutmut_33, 
        'xǁBasePopupǁpaintEvent__mutmut_34': xǁBasePopupǁpaintEvent__mutmut_34, 
        'xǁBasePopupǁpaintEvent__mutmut_35': xǁBasePopupǁpaintEvent__mutmut_35, 
        'xǁBasePopupǁpaintEvent__mutmut_36': xǁBasePopupǁpaintEvent__mutmut_36, 
        'xǁBasePopupǁpaintEvent__mutmut_37': xǁBasePopupǁpaintEvent__mutmut_37, 
        'xǁBasePopupǁpaintEvent__mutmut_38': xǁBasePopupǁpaintEvent__mutmut_38, 
        'xǁBasePopupǁpaintEvent__mutmut_39': xǁBasePopupǁpaintEvent__mutmut_39, 
        'xǁBasePopupǁpaintEvent__mutmut_40': xǁBasePopupǁpaintEvent__mutmut_40, 
        'xǁBasePopupǁpaintEvent__mutmut_41': xǁBasePopupǁpaintEvent__mutmut_41, 
        'xǁBasePopupǁpaintEvent__mutmut_42': xǁBasePopupǁpaintEvent__mutmut_42, 
        'xǁBasePopupǁpaintEvent__mutmut_43': xǁBasePopupǁpaintEvent__mutmut_43
    }
    xǁBasePopupǁpaintEvent__mutmut_orig.__name__ = 'xǁBasePopupǁpaintEvent'

    def setupUI(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁBasePopupǁsetupUI__mutmut_orig'), object.__getattribute__(self, 'xǁBasePopupǁsetupUI__mutmut_mutants'), args, kwargs, self)

    def xǁBasePopupǁsetupUI__mutmut_orig(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_1(self) -> None:
        self.vlayout = None
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_2(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(None)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_3(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName(None)
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_4(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("XXMyParentXX")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_5(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("myparent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_6(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MYPARENT")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_7(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = None
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_8(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel(None, self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_9(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", None)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_10(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_11(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", )
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_12(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("XXTest MessageXX", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_13(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("test message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_14(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("TEST MESSAGE", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_15(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = None
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_16(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(None)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_17(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_18(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(None)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_19(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet(None)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_20(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("XXcolor: #ffffff; background: transparent;XX")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_21(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("COLOR: #FFFFFF; BACKGROUND: TRANSPARENT;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_22(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(None)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_23(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(None)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_24(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(False)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_25(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(None)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_26(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = None
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_27(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(None, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_28(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, None, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_29(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, None, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_30(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, None)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_31(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_32(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_33(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_34(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, )
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_35(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(1, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_36(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 1, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_37(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 1, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_38(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 1)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_39(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(None)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_40(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(1)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_41(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(None)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_42(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(None, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_43(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, None, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_44(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, None, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_45(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, None)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_46(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_47(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_48(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_49(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, )
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_50(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(1, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_51(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 1, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_52(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 1, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_53(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 1)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_54(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = None
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_55(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton(None, self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_56(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", None)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_57(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton(self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_58(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", )
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_59(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("XXConfirmXX", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_60(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_61(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("CONFIRM", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_62(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = None

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_63(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton(None, self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_64(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", None)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_65(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton(self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_66(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", )

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_67(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("XXBackXX", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_68(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_69(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("BACK", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_70(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = None
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_71(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(None)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_72(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(15)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_73(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(None)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_74(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(None)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_75(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(61)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_76(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(None)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_77(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(None)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_78(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(61)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_79(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet(None)
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_80(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("XXbackground: transparent;XX")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_81(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("BACKGROUND: TRANSPARENT;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_82(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet(None)
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_83(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("XXbackground: transparent;XX")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_84(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("BACKGROUND: TRANSPARENT;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_85(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(None)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_86(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(None)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_87(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(None)
            self.cancel_button.clicked.connect(self.reject)
            self._update_button_style()

    def xǁBasePopupǁsetupUI__mutmut_88(self) -> None:
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.setObjectName("MyParent")
        self.label = QtWidgets.QLabel("Test Message", self)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.vlayout.addWidget(self.label)
        if self.dialog:
            self.hlauyout = QtWidgets.QHBoxLayout()
            self.hlauyout.setContentsMargins(0, 0, 0, 0)
            self.hlauyout.setSpacing(0)
            self.vlayout.addLayout(self.hlauyout)
            self.vlayout.setContentsMargins(0, 0, 0, 0)
            self.confirm_button = QtWidgets.QPushButton("Confirm", self)
            self.cancel_button = QtWidgets.QPushButton("Back", self)

            button_font = QtGui.QFont()
            button_font.setPointSize(14)
            self.confirm_button.setFont(button_font)
            self.confirm_button.setMinimumHeight(60)
            self.cancel_button.setFont(button_font)
            self.cancel_button.setMinimumHeight(60)
            self.confirm_button.setStyleSheet("background: transparent;")
            self.cancel_button.setStyleSheet("background: transparent;")
            self.hlauyout.addWidget(self.confirm_button)
            self.hlauyout.addWidget(self.cancel_button)
            self.confirm_button.clicked.connect(self.accept)
            self.cancel_button.clicked.connect(None)
            self._update_button_style()
    
    xǁBasePopupǁsetupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁBasePopupǁsetupUI__mutmut_1': xǁBasePopupǁsetupUI__mutmut_1, 
        'xǁBasePopupǁsetupUI__mutmut_2': xǁBasePopupǁsetupUI__mutmut_2, 
        'xǁBasePopupǁsetupUI__mutmut_3': xǁBasePopupǁsetupUI__mutmut_3, 
        'xǁBasePopupǁsetupUI__mutmut_4': xǁBasePopupǁsetupUI__mutmut_4, 
        'xǁBasePopupǁsetupUI__mutmut_5': xǁBasePopupǁsetupUI__mutmut_5, 
        'xǁBasePopupǁsetupUI__mutmut_6': xǁBasePopupǁsetupUI__mutmut_6, 
        'xǁBasePopupǁsetupUI__mutmut_7': xǁBasePopupǁsetupUI__mutmut_7, 
        'xǁBasePopupǁsetupUI__mutmut_8': xǁBasePopupǁsetupUI__mutmut_8, 
        'xǁBasePopupǁsetupUI__mutmut_9': xǁBasePopupǁsetupUI__mutmut_9, 
        'xǁBasePopupǁsetupUI__mutmut_10': xǁBasePopupǁsetupUI__mutmut_10, 
        'xǁBasePopupǁsetupUI__mutmut_11': xǁBasePopupǁsetupUI__mutmut_11, 
        'xǁBasePopupǁsetupUI__mutmut_12': xǁBasePopupǁsetupUI__mutmut_12, 
        'xǁBasePopupǁsetupUI__mutmut_13': xǁBasePopupǁsetupUI__mutmut_13, 
        'xǁBasePopupǁsetupUI__mutmut_14': xǁBasePopupǁsetupUI__mutmut_14, 
        'xǁBasePopupǁsetupUI__mutmut_15': xǁBasePopupǁsetupUI__mutmut_15, 
        'xǁBasePopupǁsetupUI__mutmut_16': xǁBasePopupǁsetupUI__mutmut_16, 
        'xǁBasePopupǁsetupUI__mutmut_17': xǁBasePopupǁsetupUI__mutmut_17, 
        'xǁBasePopupǁsetupUI__mutmut_18': xǁBasePopupǁsetupUI__mutmut_18, 
        'xǁBasePopupǁsetupUI__mutmut_19': xǁBasePopupǁsetupUI__mutmut_19, 
        'xǁBasePopupǁsetupUI__mutmut_20': xǁBasePopupǁsetupUI__mutmut_20, 
        'xǁBasePopupǁsetupUI__mutmut_21': xǁBasePopupǁsetupUI__mutmut_21, 
        'xǁBasePopupǁsetupUI__mutmut_22': xǁBasePopupǁsetupUI__mutmut_22, 
        'xǁBasePopupǁsetupUI__mutmut_23': xǁBasePopupǁsetupUI__mutmut_23, 
        'xǁBasePopupǁsetupUI__mutmut_24': xǁBasePopupǁsetupUI__mutmut_24, 
        'xǁBasePopupǁsetupUI__mutmut_25': xǁBasePopupǁsetupUI__mutmut_25, 
        'xǁBasePopupǁsetupUI__mutmut_26': xǁBasePopupǁsetupUI__mutmut_26, 
        'xǁBasePopupǁsetupUI__mutmut_27': xǁBasePopupǁsetupUI__mutmut_27, 
        'xǁBasePopupǁsetupUI__mutmut_28': xǁBasePopupǁsetupUI__mutmut_28, 
        'xǁBasePopupǁsetupUI__mutmut_29': xǁBasePopupǁsetupUI__mutmut_29, 
        'xǁBasePopupǁsetupUI__mutmut_30': xǁBasePopupǁsetupUI__mutmut_30, 
        'xǁBasePopupǁsetupUI__mutmut_31': xǁBasePopupǁsetupUI__mutmut_31, 
        'xǁBasePopupǁsetupUI__mutmut_32': xǁBasePopupǁsetupUI__mutmut_32, 
        'xǁBasePopupǁsetupUI__mutmut_33': xǁBasePopupǁsetupUI__mutmut_33, 
        'xǁBasePopupǁsetupUI__mutmut_34': xǁBasePopupǁsetupUI__mutmut_34, 
        'xǁBasePopupǁsetupUI__mutmut_35': xǁBasePopupǁsetupUI__mutmut_35, 
        'xǁBasePopupǁsetupUI__mutmut_36': xǁBasePopupǁsetupUI__mutmut_36, 
        'xǁBasePopupǁsetupUI__mutmut_37': xǁBasePopupǁsetupUI__mutmut_37, 
        'xǁBasePopupǁsetupUI__mutmut_38': xǁBasePopupǁsetupUI__mutmut_38, 
        'xǁBasePopupǁsetupUI__mutmut_39': xǁBasePopupǁsetupUI__mutmut_39, 
        'xǁBasePopupǁsetupUI__mutmut_40': xǁBasePopupǁsetupUI__mutmut_40, 
        'xǁBasePopupǁsetupUI__mutmut_41': xǁBasePopupǁsetupUI__mutmut_41, 
        'xǁBasePopupǁsetupUI__mutmut_42': xǁBasePopupǁsetupUI__mutmut_42, 
        'xǁBasePopupǁsetupUI__mutmut_43': xǁBasePopupǁsetupUI__mutmut_43, 
        'xǁBasePopupǁsetupUI__mutmut_44': xǁBasePopupǁsetupUI__mutmut_44, 
        'xǁBasePopupǁsetupUI__mutmut_45': xǁBasePopupǁsetupUI__mutmut_45, 
        'xǁBasePopupǁsetupUI__mutmut_46': xǁBasePopupǁsetupUI__mutmut_46, 
        'xǁBasePopupǁsetupUI__mutmut_47': xǁBasePopupǁsetupUI__mutmut_47, 
        'xǁBasePopupǁsetupUI__mutmut_48': xǁBasePopupǁsetupUI__mutmut_48, 
        'xǁBasePopupǁsetupUI__mutmut_49': xǁBasePopupǁsetupUI__mutmut_49, 
        'xǁBasePopupǁsetupUI__mutmut_50': xǁBasePopupǁsetupUI__mutmut_50, 
        'xǁBasePopupǁsetupUI__mutmut_51': xǁBasePopupǁsetupUI__mutmut_51, 
        'xǁBasePopupǁsetupUI__mutmut_52': xǁBasePopupǁsetupUI__mutmut_52, 
        'xǁBasePopupǁsetupUI__mutmut_53': xǁBasePopupǁsetupUI__mutmut_53, 
        'xǁBasePopupǁsetupUI__mutmut_54': xǁBasePopupǁsetupUI__mutmut_54, 
        'xǁBasePopupǁsetupUI__mutmut_55': xǁBasePopupǁsetupUI__mutmut_55, 
        'xǁBasePopupǁsetupUI__mutmut_56': xǁBasePopupǁsetupUI__mutmut_56, 
        'xǁBasePopupǁsetupUI__mutmut_57': xǁBasePopupǁsetupUI__mutmut_57, 
        'xǁBasePopupǁsetupUI__mutmut_58': xǁBasePopupǁsetupUI__mutmut_58, 
        'xǁBasePopupǁsetupUI__mutmut_59': xǁBasePopupǁsetupUI__mutmut_59, 
        'xǁBasePopupǁsetupUI__mutmut_60': xǁBasePopupǁsetupUI__mutmut_60, 
        'xǁBasePopupǁsetupUI__mutmut_61': xǁBasePopupǁsetupUI__mutmut_61, 
        'xǁBasePopupǁsetupUI__mutmut_62': xǁBasePopupǁsetupUI__mutmut_62, 
        'xǁBasePopupǁsetupUI__mutmut_63': xǁBasePopupǁsetupUI__mutmut_63, 
        'xǁBasePopupǁsetupUI__mutmut_64': xǁBasePopupǁsetupUI__mutmut_64, 
        'xǁBasePopupǁsetupUI__mutmut_65': xǁBasePopupǁsetupUI__mutmut_65, 
        'xǁBasePopupǁsetupUI__mutmut_66': xǁBasePopupǁsetupUI__mutmut_66, 
        'xǁBasePopupǁsetupUI__mutmut_67': xǁBasePopupǁsetupUI__mutmut_67, 
        'xǁBasePopupǁsetupUI__mutmut_68': xǁBasePopupǁsetupUI__mutmut_68, 
        'xǁBasePopupǁsetupUI__mutmut_69': xǁBasePopupǁsetupUI__mutmut_69, 
        'xǁBasePopupǁsetupUI__mutmut_70': xǁBasePopupǁsetupUI__mutmut_70, 
        'xǁBasePopupǁsetupUI__mutmut_71': xǁBasePopupǁsetupUI__mutmut_71, 
        'xǁBasePopupǁsetupUI__mutmut_72': xǁBasePopupǁsetupUI__mutmut_72, 
        'xǁBasePopupǁsetupUI__mutmut_73': xǁBasePopupǁsetupUI__mutmut_73, 
        'xǁBasePopupǁsetupUI__mutmut_74': xǁBasePopupǁsetupUI__mutmut_74, 
        'xǁBasePopupǁsetupUI__mutmut_75': xǁBasePopupǁsetupUI__mutmut_75, 
        'xǁBasePopupǁsetupUI__mutmut_76': xǁBasePopupǁsetupUI__mutmut_76, 
        'xǁBasePopupǁsetupUI__mutmut_77': xǁBasePopupǁsetupUI__mutmut_77, 
        'xǁBasePopupǁsetupUI__mutmut_78': xǁBasePopupǁsetupUI__mutmut_78, 
        'xǁBasePopupǁsetupUI__mutmut_79': xǁBasePopupǁsetupUI__mutmut_79, 
        'xǁBasePopupǁsetupUI__mutmut_80': xǁBasePopupǁsetupUI__mutmut_80, 
        'xǁBasePopupǁsetupUI__mutmut_81': xǁBasePopupǁsetupUI__mutmut_81, 
        'xǁBasePopupǁsetupUI__mutmut_82': xǁBasePopupǁsetupUI__mutmut_82, 
        'xǁBasePopupǁsetupUI__mutmut_83': xǁBasePopupǁsetupUI__mutmut_83, 
        'xǁBasePopupǁsetupUI__mutmut_84': xǁBasePopupǁsetupUI__mutmut_84, 
        'xǁBasePopupǁsetupUI__mutmut_85': xǁBasePopupǁsetupUI__mutmut_85, 
        'xǁBasePopupǁsetupUI__mutmut_86': xǁBasePopupǁsetupUI__mutmut_86, 
        'xǁBasePopupǁsetupUI__mutmut_87': xǁBasePopupǁsetupUI__mutmut_87, 
        'xǁBasePopupǁsetupUI__mutmut_88': xǁBasePopupǁsetupUI__mutmut_88
    }
    xǁBasePopupǁsetupUI__mutmut_orig.__name__ = 'xǁBasePopupǁsetupUI'
