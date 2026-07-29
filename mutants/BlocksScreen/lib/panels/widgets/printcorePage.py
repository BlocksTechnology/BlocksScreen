from lib.utils.blocks_button import BlocksCustomButton
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


class SwapPrintcorePage(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSwapPrintcorePageǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁSwapPrintcorePageǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁSwapPrintcorePageǁ__init____mutmut_orig(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "background-image: url(:/background/media/1st_background.png);"
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.repaint()
    def xǁSwapPrintcorePageǁ__init____mutmut_1(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(None)
        self.setStyleSheet(
            "background-image: url(:/background/media/1st_background.png);"
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.repaint()
    def xǁSwapPrintcorePageǁ__init____mutmut_2(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            None
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.repaint()
    def xǁSwapPrintcorePageǁ__init____mutmut_3(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "XXbackground-image: url(:/background/media/1st_background.png);XX"
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.repaint()
    def xǁSwapPrintcorePageǁ__init____mutmut_4(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "BACKGROUND-IMAGE: URL(:/BACKGROUND/MEDIA/1ST_BACKGROUND.PNG);"
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.repaint()
    def xǁSwapPrintcorePageǁ__init____mutmut_5(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "background-image: url(:/background/media/1st_background.png);"
        )
        self.setWindowFlags(
            None
        )
        self._setupUI()
        self.repaint()
    def xǁSwapPrintcorePageǁ__init____mutmut_6(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "background-image: url(:/background/media/1st_background.png);"
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup & QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.repaint()
    
    xǁSwapPrintcorePageǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSwapPrintcorePageǁ__init____mutmut_1': xǁSwapPrintcorePageǁ__init____mutmut_1, 
        'xǁSwapPrintcorePageǁ__init____mutmut_2': xǁSwapPrintcorePageǁ__init____mutmut_2, 
        'xǁSwapPrintcorePageǁ__init____mutmut_3': xǁSwapPrintcorePageǁ__init____mutmut_3, 
        'xǁSwapPrintcorePageǁ__init____mutmut_4': xǁSwapPrintcorePageǁ__init____mutmut_4, 
        'xǁSwapPrintcorePageǁ__init____mutmut_5': xǁSwapPrintcorePageǁ__init____mutmut_5, 
        'xǁSwapPrintcorePageǁ__init____mutmut_6': xǁSwapPrintcorePageǁ__init____mutmut_6
    }
    xǁSwapPrintcorePageǁ__init____mutmut_orig.__name__ = 'xǁSwapPrintcorePageǁ__init__'

    def setText(self, text: str) -> None:
        args = [text]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSwapPrintcorePageǁsetText__mutmut_orig'), object.__getattribute__(self, 'xǁSwapPrintcorePageǁsetText__mutmut_mutants'), args, kwargs, self)

    def xǁSwapPrintcorePageǁsetText__mutmut_orig(self, text: str) -> None:
        """Set widget text"""
        self.label.setText(text)
        self.repaint()

    def xǁSwapPrintcorePageǁsetText__mutmut_1(self, text: str) -> None:
        """Set widget text"""
        self.label.setText(None)
        self.repaint()
    
    xǁSwapPrintcorePageǁsetText__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSwapPrintcorePageǁsetText__mutmut_1': xǁSwapPrintcorePageǁsetText__mutmut_1
    }
    xǁSwapPrintcorePageǁsetText__mutmut_orig.__name__ = 'xǁSwapPrintcorePageǁsetText'

    def text(self) -> str:
        """Return current widget text"""
        return self.label.text()

    def _geometry_calc(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_orig'), object.__getattribute__(self, 'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_mutants'), args, kwargs, self)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_orig(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_1(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = None
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_2(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_3(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None or app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_4(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is not None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_5(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = None
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_6(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = None
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_7(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = None
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_8(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = None
        height = main_window.height()

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_9(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = None

        self.setGeometry(x, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_10(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(None, y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_11(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, None, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_12(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, None, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_13(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, None)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_14(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(y, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_15(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, width, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_16(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, height)

    def xǁSwapPrintcorePageǁ_geometry_calc__mutmut_17(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        x = main_window.geometry().x()
        y = main_window.geometry().y()
        width = main_window.width()
        height = main_window.height()

        self.setGeometry(x, y, width, )
    
    xǁSwapPrintcorePageǁ_geometry_calc__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_1': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_1, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_2': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_2, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_3': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_3, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_4': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_4, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_5': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_5, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_6': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_6, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_7': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_7, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_8': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_8, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_9': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_9, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_10': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_10, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_11': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_11, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_12': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_12, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_13': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_13, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_14': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_14, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_15': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_15, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_16': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_16, 
        'xǁSwapPrintcorePageǁ_geometry_calc__mutmut_17': xǁSwapPrintcorePageǁ_geometry_calc__mutmut_17
    }
    xǁSwapPrintcorePageǁ_geometry_calc__mutmut_orig.__name__ = 'xǁSwapPrintcorePageǁ_geometry_calc'

    def sizeHint(self) -> QtCore.QSize:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSwapPrintcorePageǁsizeHint__mutmut_orig'), object.__getattribute__(self, 'xǁSwapPrintcorePageǁsizeHint__mutmut_mutants'), args, kwargs, self)

    def xǁSwapPrintcorePageǁsizeHint__mutmut_orig(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_1(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = None
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_2(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(None)
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_3(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = None
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_4(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(None)
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_5(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = None
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_6(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = None
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_7(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() - (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_8(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) / 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_9(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() + popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_10(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 3
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_11(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(None, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_12(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, None)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_13(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_14(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, )
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_15(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(None, popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_16(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, None)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_17(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_height)
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_18(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, )
        self.setMinimumSize(popup_width, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_19(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(None, popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_20(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, None)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_21(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_height)

        return super().sizeHint()

    def xǁSwapPrintcorePageǁsizeHint__mutmut_22(self) -> QtCore.QSize:
        """Re-implemented method, handle widget size"""
        popup_width = int(self.geometry().width())
        popup_height = int(self.geometry().height())
        # Centering logic

        popup_x = self.x()
        popup_y = self.y() + (self.height() - popup_height) // 2
        self.move(popup_x, popup_y)
        self.setFixedSize(popup_width, popup_height)
        self.setMinimumSize(popup_width, )

        return super().sizeHint()
    
    xǁSwapPrintcorePageǁsizeHint__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSwapPrintcorePageǁsizeHint__mutmut_1': xǁSwapPrintcorePageǁsizeHint__mutmut_1, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_2': xǁSwapPrintcorePageǁsizeHint__mutmut_2, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_3': xǁSwapPrintcorePageǁsizeHint__mutmut_3, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_4': xǁSwapPrintcorePageǁsizeHint__mutmut_4, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_5': xǁSwapPrintcorePageǁsizeHint__mutmut_5, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_6': xǁSwapPrintcorePageǁsizeHint__mutmut_6, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_7': xǁSwapPrintcorePageǁsizeHint__mutmut_7, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_8': xǁSwapPrintcorePageǁsizeHint__mutmut_8, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_9': xǁSwapPrintcorePageǁsizeHint__mutmut_9, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_10': xǁSwapPrintcorePageǁsizeHint__mutmut_10, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_11': xǁSwapPrintcorePageǁsizeHint__mutmut_11, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_12': xǁSwapPrintcorePageǁsizeHint__mutmut_12, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_13': xǁSwapPrintcorePageǁsizeHint__mutmut_13, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_14': xǁSwapPrintcorePageǁsizeHint__mutmut_14, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_15': xǁSwapPrintcorePageǁsizeHint__mutmut_15, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_16': xǁSwapPrintcorePageǁsizeHint__mutmut_16, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_17': xǁSwapPrintcorePageǁsizeHint__mutmut_17, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_18': xǁSwapPrintcorePageǁsizeHint__mutmut_18, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_19': xǁSwapPrintcorePageǁsizeHint__mutmut_19, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_20': xǁSwapPrintcorePageǁsizeHint__mutmut_20, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_21': xǁSwapPrintcorePageǁsizeHint__mutmut_21, 
        'xǁSwapPrintcorePageǁsizeHint__mutmut_22': xǁSwapPrintcorePageǁsizeHint__mutmut_22
    }
    xǁSwapPrintcorePageǁsizeHint__mutmut_orig.__name__ = 'xǁSwapPrintcorePageǁsizeHint'

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSwapPrintcorePageǁresizeEvent__mutmut_orig'), object.__getattribute__(self, 'xǁSwapPrintcorePageǁresizeEvent__mutmut_mutants'), args, kwargs, self)

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_orig(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_1(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(None)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_2(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(None, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_3(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, None, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_4(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, None, 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_5(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), None)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_6(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_7(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_8(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_9(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), )
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_10(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(1, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_11(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 1, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_12(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 61)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_13(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = None
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_14(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 21
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_15(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = None
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_16(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) + label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_17(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(None) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_18(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() / 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_19(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 1.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_20(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            None, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_21(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, None, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_22(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, None, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_23(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, None
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_24(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_25(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_26(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_27(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_28(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 61, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_29(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() + 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_30(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 / label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_31(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 3 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_32(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = None
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_33(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 251
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_34(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = None
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_35(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 81
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_36(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = None
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_37(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 101
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_38(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = None
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_39(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width - spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_40(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 / button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_41(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 3 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_42(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = None
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_43(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) / 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_44(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() + total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_45(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 3
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_46(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = None
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_47(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height + 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_48(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() + button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_49(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 46
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_50(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(None, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_51(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, None, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_52(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, None, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_53(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, None)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_54(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_55(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_56(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_57(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, )
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_58(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            None, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_59(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, None, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_60(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, None, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_61(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, None
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_62(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_63(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_64(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_65(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 100, button_y, button_width, )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_66(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width - 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_67(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x - button_width + 100, button_y, button_width, button_height
        )

    def xǁSwapPrintcorePageǁresizeEvent__mutmut_68(self, event: QtGui.QResizeEvent) -> None:
        """Re-implemented method, handle widget resize event"""
        super().resizeEvent(event)
        self.tittle.setGeometry(0, 0, self.width(), 60)
        label_margin = 20
        label_height = int(self.height() * 0.65) - label_margin
        self.label.setGeometry(
            label_margin, 60, self.width() - 2 * label_margin, label_height
        )
        button_width = 250
        button_height = 80
        spacing = 100
        total_button_width = 2 * button_width + spacing
        start_x = (self.width() - total_button_width) // 2
        button_y = self.height() - button_height - 45
        self.pc_accept.setGeometry(start_x, button_y, button_width, button_height)
        self.pc_cancel.setGeometry(
            start_x + button_width + 101, button_y, button_width, button_height
        )
    
    xǁSwapPrintcorePageǁresizeEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSwapPrintcorePageǁresizeEvent__mutmut_1': xǁSwapPrintcorePageǁresizeEvent__mutmut_1, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_2': xǁSwapPrintcorePageǁresizeEvent__mutmut_2, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_3': xǁSwapPrintcorePageǁresizeEvent__mutmut_3, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_4': xǁSwapPrintcorePageǁresizeEvent__mutmut_4, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_5': xǁSwapPrintcorePageǁresizeEvent__mutmut_5, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_6': xǁSwapPrintcorePageǁresizeEvent__mutmut_6, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_7': xǁSwapPrintcorePageǁresizeEvent__mutmut_7, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_8': xǁSwapPrintcorePageǁresizeEvent__mutmut_8, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_9': xǁSwapPrintcorePageǁresizeEvent__mutmut_9, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_10': xǁSwapPrintcorePageǁresizeEvent__mutmut_10, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_11': xǁSwapPrintcorePageǁresizeEvent__mutmut_11, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_12': xǁSwapPrintcorePageǁresizeEvent__mutmut_12, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_13': xǁSwapPrintcorePageǁresizeEvent__mutmut_13, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_14': xǁSwapPrintcorePageǁresizeEvent__mutmut_14, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_15': xǁSwapPrintcorePageǁresizeEvent__mutmut_15, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_16': xǁSwapPrintcorePageǁresizeEvent__mutmut_16, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_17': xǁSwapPrintcorePageǁresizeEvent__mutmut_17, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_18': xǁSwapPrintcorePageǁresizeEvent__mutmut_18, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_19': xǁSwapPrintcorePageǁresizeEvent__mutmut_19, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_20': xǁSwapPrintcorePageǁresizeEvent__mutmut_20, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_21': xǁSwapPrintcorePageǁresizeEvent__mutmut_21, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_22': xǁSwapPrintcorePageǁresizeEvent__mutmut_22, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_23': xǁSwapPrintcorePageǁresizeEvent__mutmut_23, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_24': xǁSwapPrintcorePageǁresizeEvent__mutmut_24, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_25': xǁSwapPrintcorePageǁresizeEvent__mutmut_25, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_26': xǁSwapPrintcorePageǁresizeEvent__mutmut_26, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_27': xǁSwapPrintcorePageǁresizeEvent__mutmut_27, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_28': xǁSwapPrintcorePageǁresizeEvent__mutmut_28, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_29': xǁSwapPrintcorePageǁresizeEvent__mutmut_29, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_30': xǁSwapPrintcorePageǁresizeEvent__mutmut_30, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_31': xǁSwapPrintcorePageǁresizeEvent__mutmut_31, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_32': xǁSwapPrintcorePageǁresizeEvent__mutmut_32, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_33': xǁSwapPrintcorePageǁresizeEvent__mutmut_33, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_34': xǁSwapPrintcorePageǁresizeEvent__mutmut_34, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_35': xǁSwapPrintcorePageǁresizeEvent__mutmut_35, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_36': xǁSwapPrintcorePageǁresizeEvent__mutmut_36, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_37': xǁSwapPrintcorePageǁresizeEvent__mutmut_37, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_38': xǁSwapPrintcorePageǁresizeEvent__mutmut_38, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_39': xǁSwapPrintcorePageǁresizeEvent__mutmut_39, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_40': xǁSwapPrintcorePageǁresizeEvent__mutmut_40, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_41': xǁSwapPrintcorePageǁresizeEvent__mutmut_41, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_42': xǁSwapPrintcorePageǁresizeEvent__mutmut_42, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_43': xǁSwapPrintcorePageǁresizeEvent__mutmut_43, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_44': xǁSwapPrintcorePageǁresizeEvent__mutmut_44, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_45': xǁSwapPrintcorePageǁresizeEvent__mutmut_45, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_46': xǁSwapPrintcorePageǁresizeEvent__mutmut_46, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_47': xǁSwapPrintcorePageǁresizeEvent__mutmut_47, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_48': xǁSwapPrintcorePageǁresizeEvent__mutmut_48, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_49': xǁSwapPrintcorePageǁresizeEvent__mutmut_49, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_50': xǁSwapPrintcorePageǁresizeEvent__mutmut_50, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_51': xǁSwapPrintcorePageǁresizeEvent__mutmut_51, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_52': xǁSwapPrintcorePageǁresizeEvent__mutmut_52, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_53': xǁSwapPrintcorePageǁresizeEvent__mutmut_53, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_54': xǁSwapPrintcorePageǁresizeEvent__mutmut_54, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_55': xǁSwapPrintcorePageǁresizeEvent__mutmut_55, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_56': xǁSwapPrintcorePageǁresizeEvent__mutmut_56, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_57': xǁSwapPrintcorePageǁresizeEvent__mutmut_57, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_58': xǁSwapPrintcorePageǁresizeEvent__mutmut_58, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_59': xǁSwapPrintcorePageǁresizeEvent__mutmut_59, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_60': xǁSwapPrintcorePageǁresizeEvent__mutmut_60, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_61': xǁSwapPrintcorePageǁresizeEvent__mutmut_61, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_62': xǁSwapPrintcorePageǁresizeEvent__mutmut_62, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_63': xǁSwapPrintcorePageǁresizeEvent__mutmut_63, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_64': xǁSwapPrintcorePageǁresizeEvent__mutmut_64, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_65': xǁSwapPrintcorePageǁresizeEvent__mutmut_65, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_66': xǁSwapPrintcorePageǁresizeEvent__mutmut_66, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_67': xǁSwapPrintcorePageǁresizeEvent__mutmut_67, 
        'xǁSwapPrintcorePageǁresizeEvent__mutmut_68': xǁSwapPrintcorePageǁresizeEvent__mutmut_68
    }
    xǁSwapPrintcorePageǁresizeEvent__mutmut_orig.__name__ = 'xǁSwapPrintcorePageǁresizeEvent'

    def show(self) -> None:
        """Re-implemented method, widget show"""
        self._geometry_calc()
        self.repaint()
        return super().show()

    def _setupUI(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁSwapPrintcorePageǁ_setupUI__mutmut_orig'), object.__getattribute__(self, 'xǁSwapPrintcorePageǁ_setupUI__mutmut_mutants'), args, kwargs, self)

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_orig(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_1(self) -> None:
        font = None
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_2(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(None)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_3(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(21)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_4(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = None
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_5(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel(None, self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_6(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", None)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_7(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel(self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_8(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", )
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_9(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("XXSwap PrintcoreXX", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_10(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("swap printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_11(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("SWAP PRINTCORE", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_12(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(None)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_13(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet(None)
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_14(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("XXcolor: #ffffff; background: transparent;XX")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_15(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("COLOR: #FFFFFF; BACKGROUND: TRANSPARENT;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_16(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(None)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_17(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = None
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_18(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel(None, self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_19(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", None)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_20(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel(self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_21(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", )
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_22(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("XXinsert smth here laterXX", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_23(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("INSERT SMTH HERE LATER", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_24(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(None)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_25(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet(None)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_26(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("XXcolor: #ffffff; background: transparent;XX")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_27(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("COLOR: #FFFFFF; BACKGROUND: TRANSPARENT;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_28(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(None)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_29(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(None)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_30(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(16)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_31(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = None
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_32(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=None)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_33(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(None)
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_34(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(None, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_35(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, None))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_36(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_37(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, ))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_38(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(251, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_39(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 81))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_40(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(None)
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_41(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(None, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_42(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, None))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_43(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_44(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, ))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_45(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(251, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_46(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 81))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_47(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            None, QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_48(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", None
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_49(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_50(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_51(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "XXicon_pixmapXX", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_52(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "ICON_PIXMAP", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_53(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(None)
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_54(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap("XX:/dialog/media/btn_icons/no.svgXX")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_55(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/DIALOG/MEDIA/BTN_ICONS/NO.SVG")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_56(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName(None)
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_57(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("XXpc_cancelXX")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_58(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("PC_CANCEL")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_59(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(None)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_60(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText(None)

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_61(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("XXCancelXX")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_62(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_63(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("CANCEL")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_64(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = None
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_65(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=None)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_66(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(None)
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_67(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(None, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_68(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, None))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_69(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_70(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, ))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_71(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(251, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_72(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 81))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_73(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(None)
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_74(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(None, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_75(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, None))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_76(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_77(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, ))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_78(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(251, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_79(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 81))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_80(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            None, QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_81(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", None
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_82(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_83(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_84(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "XXicon_pixmapXX", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_85(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "ICON_PIXMAP", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_86(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(None)
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_87(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap("XX:/dialog/media/btn_icons/yes.svgXX")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_88(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/DIALOG/MEDIA/BTN_ICONS/YES.SVG")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_89(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName(None)
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_90(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("XXpc_acceptXX")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_91(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("PC_ACCEPT")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_92(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(None)
        self.pc_accept.setText("Continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_93(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText(None)

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_94(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("XXContinue?XX")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_95(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("continue?")

    def xǁSwapPrintcorePageǁ_setupUI__mutmut_96(self) -> None:
        font = QtGui.QFont()
        font.setPointSize(20)

        self.tittle = QtWidgets.QLabel("Swap Printcore", self)
        self.tittle.setFont(font)
        self.tittle.setStyleSheet("color: #ffffff; background: transparent;")
        self.tittle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel("insert smth here later", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #ffffff; background: transparent;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        font.setPointSize(15)

        self.pc_cancel = BlocksCustomButton(parent=self)
        self.pc_cancel.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_cancel.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/no.svg")
        )
        self.pc_cancel.setObjectName("pc_cancel")
        self.pc_cancel.setFont(font)
        self.pc_cancel.setText("Cancel")

        self.pc_accept = BlocksCustomButton(parent=self)
        self.pc_accept.setMinimumSize(QtCore.QSize(250, 80))
        self.pc_accept.setMaximumSize(QtCore.QSize(250, 80))
        self.pc_accept.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/dialog/media/btn_icons/yes.svg")
        )
        self.pc_accept.setObjectName("pc_accept")
        self.pc_accept.setFont(font)
        self.pc_accept.setText("CONTINUE?")
    
    xǁSwapPrintcorePageǁ_setupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁSwapPrintcorePageǁ_setupUI__mutmut_1': xǁSwapPrintcorePageǁ_setupUI__mutmut_1, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_2': xǁSwapPrintcorePageǁ_setupUI__mutmut_2, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_3': xǁSwapPrintcorePageǁ_setupUI__mutmut_3, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_4': xǁSwapPrintcorePageǁ_setupUI__mutmut_4, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_5': xǁSwapPrintcorePageǁ_setupUI__mutmut_5, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_6': xǁSwapPrintcorePageǁ_setupUI__mutmut_6, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_7': xǁSwapPrintcorePageǁ_setupUI__mutmut_7, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_8': xǁSwapPrintcorePageǁ_setupUI__mutmut_8, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_9': xǁSwapPrintcorePageǁ_setupUI__mutmut_9, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_10': xǁSwapPrintcorePageǁ_setupUI__mutmut_10, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_11': xǁSwapPrintcorePageǁ_setupUI__mutmut_11, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_12': xǁSwapPrintcorePageǁ_setupUI__mutmut_12, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_13': xǁSwapPrintcorePageǁ_setupUI__mutmut_13, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_14': xǁSwapPrintcorePageǁ_setupUI__mutmut_14, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_15': xǁSwapPrintcorePageǁ_setupUI__mutmut_15, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_16': xǁSwapPrintcorePageǁ_setupUI__mutmut_16, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_17': xǁSwapPrintcorePageǁ_setupUI__mutmut_17, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_18': xǁSwapPrintcorePageǁ_setupUI__mutmut_18, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_19': xǁSwapPrintcorePageǁ_setupUI__mutmut_19, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_20': xǁSwapPrintcorePageǁ_setupUI__mutmut_20, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_21': xǁSwapPrintcorePageǁ_setupUI__mutmut_21, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_22': xǁSwapPrintcorePageǁ_setupUI__mutmut_22, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_23': xǁSwapPrintcorePageǁ_setupUI__mutmut_23, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_24': xǁSwapPrintcorePageǁ_setupUI__mutmut_24, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_25': xǁSwapPrintcorePageǁ_setupUI__mutmut_25, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_26': xǁSwapPrintcorePageǁ_setupUI__mutmut_26, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_27': xǁSwapPrintcorePageǁ_setupUI__mutmut_27, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_28': xǁSwapPrintcorePageǁ_setupUI__mutmut_28, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_29': xǁSwapPrintcorePageǁ_setupUI__mutmut_29, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_30': xǁSwapPrintcorePageǁ_setupUI__mutmut_30, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_31': xǁSwapPrintcorePageǁ_setupUI__mutmut_31, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_32': xǁSwapPrintcorePageǁ_setupUI__mutmut_32, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_33': xǁSwapPrintcorePageǁ_setupUI__mutmut_33, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_34': xǁSwapPrintcorePageǁ_setupUI__mutmut_34, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_35': xǁSwapPrintcorePageǁ_setupUI__mutmut_35, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_36': xǁSwapPrintcorePageǁ_setupUI__mutmut_36, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_37': xǁSwapPrintcorePageǁ_setupUI__mutmut_37, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_38': xǁSwapPrintcorePageǁ_setupUI__mutmut_38, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_39': xǁSwapPrintcorePageǁ_setupUI__mutmut_39, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_40': xǁSwapPrintcorePageǁ_setupUI__mutmut_40, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_41': xǁSwapPrintcorePageǁ_setupUI__mutmut_41, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_42': xǁSwapPrintcorePageǁ_setupUI__mutmut_42, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_43': xǁSwapPrintcorePageǁ_setupUI__mutmut_43, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_44': xǁSwapPrintcorePageǁ_setupUI__mutmut_44, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_45': xǁSwapPrintcorePageǁ_setupUI__mutmut_45, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_46': xǁSwapPrintcorePageǁ_setupUI__mutmut_46, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_47': xǁSwapPrintcorePageǁ_setupUI__mutmut_47, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_48': xǁSwapPrintcorePageǁ_setupUI__mutmut_48, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_49': xǁSwapPrintcorePageǁ_setupUI__mutmut_49, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_50': xǁSwapPrintcorePageǁ_setupUI__mutmut_50, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_51': xǁSwapPrintcorePageǁ_setupUI__mutmut_51, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_52': xǁSwapPrintcorePageǁ_setupUI__mutmut_52, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_53': xǁSwapPrintcorePageǁ_setupUI__mutmut_53, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_54': xǁSwapPrintcorePageǁ_setupUI__mutmut_54, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_55': xǁSwapPrintcorePageǁ_setupUI__mutmut_55, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_56': xǁSwapPrintcorePageǁ_setupUI__mutmut_56, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_57': xǁSwapPrintcorePageǁ_setupUI__mutmut_57, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_58': xǁSwapPrintcorePageǁ_setupUI__mutmut_58, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_59': xǁSwapPrintcorePageǁ_setupUI__mutmut_59, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_60': xǁSwapPrintcorePageǁ_setupUI__mutmut_60, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_61': xǁSwapPrintcorePageǁ_setupUI__mutmut_61, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_62': xǁSwapPrintcorePageǁ_setupUI__mutmut_62, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_63': xǁSwapPrintcorePageǁ_setupUI__mutmut_63, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_64': xǁSwapPrintcorePageǁ_setupUI__mutmut_64, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_65': xǁSwapPrintcorePageǁ_setupUI__mutmut_65, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_66': xǁSwapPrintcorePageǁ_setupUI__mutmut_66, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_67': xǁSwapPrintcorePageǁ_setupUI__mutmut_67, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_68': xǁSwapPrintcorePageǁ_setupUI__mutmut_68, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_69': xǁSwapPrintcorePageǁ_setupUI__mutmut_69, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_70': xǁSwapPrintcorePageǁ_setupUI__mutmut_70, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_71': xǁSwapPrintcorePageǁ_setupUI__mutmut_71, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_72': xǁSwapPrintcorePageǁ_setupUI__mutmut_72, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_73': xǁSwapPrintcorePageǁ_setupUI__mutmut_73, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_74': xǁSwapPrintcorePageǁ_setupUI__mutmut_74, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_75': xǁSwapPrintcorePageǁ_setupUI__mutmut_75, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_76': xǁSwapPrintcorePageǁ_setupUI__mutmut_76, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_77': xǁSwapPrintcorePageǁ_setupUI__mutmut_77, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_78': xǁSwapPrintcorePageǁ_setupUI__mutmut_78, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_79': xǁSwapPrintcorePageǁ_setupUI__mutmut_79, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_80': xǁSwapPrintcorePageǁ_setupUI__mutmut_80, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_81': xǁSwapPrintcorePageǁ_setupUI__mutmut_81, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_82': xǁSwapPrintcorePageǁ_setupUI__mutmut_82, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_83': xǁSwapPrintcorePageǁ_setupUI__mutmut_83, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_84': xǁSwapPrintcorePageǁ_setupUI__mutmut_84, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_85': xǁSwapPrintcorePageǁ_setupUI__mutmut_85, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_86': xǁSwapPrintcorePageǁ_setupUI__mutmut_86, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_87': xǁSwapPrintcorePageǁ_setupUI__mutmut_87, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_88': xǁSwapPrintcorePageǁ_setupUI__mutmut_88, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_89': xǁSwapPrintcorePageǁ_setupUI__mutmut_89, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_90': xǁSwapPrintcorePageǁ_setupUI__mutmut_90, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_91': xǁSwapPrintcorePageǁ_setupUI__mutmut_91, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_92': xǁSwapPrintcorePageǁ_setupUI__mutmut_92, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_93': xǁSwapPrintcorePageǁ_setupUI__mutmut_93, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_94': xǁSwapPrintcorePageǁ_setupUI__mutmut_94, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_95': xǁSwapPrintcorePageǁ_setupUI__mutmut_95, 
        'xǁSwapPrintcorePageǁ_setupUI__mutmut_96': xǁSwapPrintcorePageǁ_setupUI__mutmut_96
    }
    xǁSwapPrintcorePageǁ_setupUI__mutmut_orig.__name__ = 'xǁSwapPrintcorePageǁ_setupUI'
