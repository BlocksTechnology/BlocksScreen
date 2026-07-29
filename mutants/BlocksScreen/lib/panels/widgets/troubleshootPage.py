from PyQt6 import QtCore, QtGui, QtWidgets

from lib.utils.icon_button import IconButton
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


class TroubleshootPage(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTroubleshootPageǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁTroubleshootPageǁ__init____mutmut_mutants'), args, kwargs, self)
    def xǁTroubleshootPageǁ__init____mutmut_orig(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            "For more information check our website \n www.blockstec.com \n or \nsupport@blockstec.com"
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_1(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(None)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            "For more information check our website \n www.blockstec.com \n or \nsupport@blockstec.com"
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_2(
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
        self.label_4.setText(
            "For more information check our website \n www.blockstec.com \n or \nsupport@blockstec.com"
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_3(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            None
        )
        self._setupUI()
        self.label_4.setText(
            "For more information check our website \n www.blockstec.com \n or \nsupport@blockstec.com"
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_4(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup & QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            "For more information check our website \n www.blockstec.com \n or \nsupport@blockstec.com"
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_5(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            None
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_6(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            "XXFor more information check our website \n www.blockstec.com \n or \nsupport@blockstec.comXX"
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_7(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            "for more information check our website \n www.blockstec.com \n or \nsupport@blockstec.com"
        )
        self.repaint()
    def xǁTroubleshootPageǁ__init____mutmut_8(
        self,
        parent: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            """
            #troubleshoot_page { 
                background-image: url(:/background/media/1st_background.png); 
                border: none;
            }
            """
        )
        self.setWindowFlags(
            QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint
        )
        self._setupUI()
        self.label_4.setText(
            "FOR MORE INFORMATION CHECK OUR WEBSITE \n WWW.BLOCKSTEC.COM \n OR \nSUPPORT@BLOCKSTEC.COM"
        )
        self.repaint()
    
    xǁTroubleshootPageǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTroubleshootPageǁ__init____mutmut_1': xǁTroubleshootPageǁ__init____mutmut_1, 
        'xǁTroubleshootPageǁ__init____mutmut_2': xǁTroubleshootPageǁ__init____mutmut_2, 
        'xǁTroubleshootPageǁ__init____mutmut_3': xǁTroubleshootPageǁ__init____mutmut_3, 
        'xǁTroubleshootPageǁ__init____mutmut_4': xǁTroubleshootPageǁ__init____mutmut_4, 
        'xǁTroubleshootPageǁ__init____mutmut_5': xǁTroubleshootPageǁ__init____mutmut_5, 
        'xǁTroubleshootPageǁ__init____mutmut_6': xǁTroubleshootPageǁ__init____mutmut_6, 
        'xǁTroubleshootPageǁ__init____mutmut_7': xǁTroubleshootPageǁ__init____mutmut_7, 
        'xǁTroubleshootPageǁ__init____mutmut_8': xǁTroubleshootPageǁ__init____mutmut_8
    }
    xǁTroubleshootPageǁ__init____mutmut_orig.__name__ = 'xǁTroubleshootPageǁ__init__'

    def _geometry_calc(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTroubleshootPageǁ_geometry_calc__mutmut_orig'), object.__getattribute__(self, 'xǁTroubleshootPageǁ_geometry_calc__mutmut_mutants'), args, kwargs, self)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_orig(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_1(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = None
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_2(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_3(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None or app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_4(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is not None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_5(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = None
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_6(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = None
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_7(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = None
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_8(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = None
            height = main_window.height()
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_9(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = None
            self.setGeometry(x, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_10(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(None, y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_11(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, None, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_12(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, None, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_13(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, None)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_14(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(y, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_15(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, width, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_16(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, height)

    def xǁTroubleshootPageǁ_geometry_calc__mutmut_17(self) -> None:
        """Calculate widget position relative to the screen"""
        app_instance = QtWidgets.QApplication.instance()
        main_window = app_instance.activeWindow() if app_instance else None
        if main_window is None and app_instance:
            for widget in app_instance.allWidgets():
                if isinstance(widget, QtWidgets.QMainWindow):
                    main_window = widget
        if main_window:
            x = main_window.geometry().x()
            y = main_window.geometry().y()
            width = main_window.width()
            height = main_window.height()
            self.setGeometry(x, y, width, )
    
    xǁTroubleshootPageǁ_geometry_calc__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTroubleshootPageǁ_geometry_calc__mutmut_1': xǁTroubleshootPageǁ_geometry_calc__mutmut_1, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_2': xǁTroubleshootPageǁ_geometry_calc__mutmut_2, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_3': xǁTroubleshootPageǁ_geometry_calc__mutmut_3, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_4': xǁTroubleshootPageǁ_geometry_calc__mutmut_4, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_5': xǁTroubleshootPageǁ_geometry_calc__mutmut_5, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_6': xǁTroubleshootPageǁ_geometry_calc__mutmut_6, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_7': xǁTroubleshootPageǁ_geometry_calc__mutmut_7, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_8': xǁTroubleshootPageǁ_geometry_calc__mutmut_8, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_9': xǁTroubleshootPageǁ_geometry_calc__mutmut_9, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_10': xǁTroubleshootPageǁ_geometry_calc__mutmut_10, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_11': xǁTroubleshootPageǁ_geometry_calc__mutmut_11, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_12': xǁTroubleshootPageǁ_geometry_calc__mutmut_12, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_13': xǁTroubleshootPageǁ_geometry_calc__mutmut_13, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_14': xǁTroubleshootPageǁ_geometry_calc__mutmut_14, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_15': xǁTroubleshootPageǁ_geometry_calc__mutmut_15, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_16': xǁTroubleshootPageǁ_geometry_calc__mutmut_16, 
        'xǁTroubleshootPageǁ_geometry_calc__mutmut_17': xǁTroubleshootPageǁ_geometry_calc__mutmut_17
    }
    xǁTroubleshootPageǁ_geometry_calc__mutmut_orig.__name__ = 'xǁTroubleshootPageǁ_geometry_calc'

    def show(self) -> None:
        """Re-implemented method, widget show"""
        self._geometry_calc()
        self.repaint()
        return super().show()

    def _setupUI(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁTroubleshootPageǁ_setupUI__mutmut_orig'), object.__getattribute__(self, 'xǁTroubleshootPageǁ_setupUI__mutmut_mutants'), args, kwargs, self)

    def xǁTroubleshootPageǁ_setupUI__mutmut_orig(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_1(self) -> None:
        self.setObjectName(None)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_2(self) -> None:
        self.setObjectName("XXtroubleshoot_pageXX")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_3(self) -> None:
        self.setObjectName("TROUBLESHOOT_PAGE")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_4(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = None
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_5(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(None)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_6(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName(None)
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_7(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("XXverticalLayoutXX")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_8(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticallayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_9(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("VERTICALLAYOUT")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_10(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = None
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_11(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName(None)
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_12(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("XXleds_slider_header_layout_2XX")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_13(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("LEDS_SLIDER_HEADER_LAYOUT_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_14(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = None
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_15(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            None,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_16(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            None,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_17(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            None,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_18(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            None,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_19(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_20(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_21(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_22(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_23(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            61,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_24(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            61,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_25(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(None)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_26(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = None
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_27(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            None,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_28(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            None,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_29(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            None,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_30(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            None,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_31(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_32(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_33(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_34(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_35(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            182,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_36(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            61,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_37(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(None)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_38(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = None
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_39(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel(None, parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_40(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=None)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_41(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel(parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_42(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", )
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_43(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("XXTroubleshootXX", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_44(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_45(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("TROUBLESHOOT", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_46(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(None)
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_47(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(None, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_48(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, None))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_49(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_50(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, ))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_51(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(1, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_52(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 61))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_53(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(None)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_54(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(None, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_55(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, None))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_56(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_57(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, ))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_58(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777216, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_59(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 61))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_60(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = None
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_61(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily(None)
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_62(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("XXMomcakeXX")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_63(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_64(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("MOMCAKE")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_65(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(None)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_66(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(25)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_67(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(None)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_68(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet(None)
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_69(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("XXbackground: transparent; color: white;XX")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_70(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("BACKGROUND: TRANSPARENT; COLOR: WHITE;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_71(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(None)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_72(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName(None)
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_73(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("XXtb_tittle_labelXX")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_74(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("TB_TITTLE_LABEL")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_75(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(None)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_76(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = None
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_77(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            None,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_78(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            None,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_79(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            None,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_80(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            None,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_81(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_82(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_83(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_84(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_85(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            1,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_86(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            61,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_87(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(None)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_88(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = None
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_89(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=None)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_90(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = None
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_91(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            None,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_92(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            None,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_93(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_94(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_95(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(None)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_96(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_97(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(None)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_98(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_99(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(None)
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_100(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(None)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_101(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(None)
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_102(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(None, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_103(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, None))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_104(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_105(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, ))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_106(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(61, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_107(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 61))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_108(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(None)
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_109(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(None, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_110(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, None))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_111(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_112(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, ))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_113(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(61, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_114(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 61))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_115(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = None
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_116(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily(None)
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_117(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("XXMomcakeXX")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_118(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_119(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("MOMCAKE")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_120(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(None)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_121(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(25)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_122(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(None)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_123(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(True)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_124(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(None)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_125(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(None)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_126(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(None)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_127(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(True)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_128(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(None)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_129(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(False)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_130(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(None)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_131(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(None)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_132(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet(None)
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_133(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("XXXX")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_134(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(None)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_135(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(True)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_136(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(None)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_137(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(False)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_138(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            None, QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_139(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", None
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_140(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_141(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_142(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "XXicon_pixmapXX", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_143(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "ICON_PIXMAP", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_144(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(None)
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_145(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap("XX:/ui/media/btn_icons/back.svgXX")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_146(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/UI/MEDIA/BTN_ICONS/BACK.SVG")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_147(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName(None)
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_148(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("XXtb_back_btnXX")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_149(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("TB_BACK_BTN")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_150(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(None)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_151(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(None)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_152(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = None
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_153(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(None)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_154(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("XXhorizontalLayoutXX")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_155(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontallayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_156(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("HORIZONTALLAYOUT")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_157(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = None
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_158(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName(None)
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_159(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("XXverticalLayout_10XX")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_160(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticallayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_161(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("VERTICALLAYOUT_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_162(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = None
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_163(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel(None, parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_164(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=None)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_165(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_166(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_167(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("XXidk whar to type thisXX", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_168(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("IDK WHAR TO TYPE THIS", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_169(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = None
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_170(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            None,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_171(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            None,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_172(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_173(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_174(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(None)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_175(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_176(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(None)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_177(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_178(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(None)
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_179(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(None)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_180(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = None
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_181(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(None)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_182(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_183(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(None)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_184(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(None)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_185(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("XXcolor:whiteXX")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_186(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("COLOR:WHITE")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_187(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(None)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_188(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName(None)
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_189(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("XXlabel_4XX")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_190(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("LABEL_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_191(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(None)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_192(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(None)
        self.verticalLayout.addLayout(self.horizontalLayout)

    def xǁTroubleshootPageǁ_setupUI__mutmut_193(self) -> None:
        self.setObjectName("troubleshoot_page")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leds_slider_header_layout_2 = QtWidgets.QHBoxLayout()
        self.leds_slider_header_layout_2.setObjectName("leds_slider_header_layout_2")
        spacerItem18 = QtWidgets.QSpacerItem(
            60,
            60,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem18)
        spacerItem19 = QtWidgets.QSpacerItem(
            181,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem19)
        self.tb_tittle_label = QtWidgets.QLabel("Troubleshoot", parent=self)
        self.tb_tittle_label.setMinimumSize(QtCore.QSize(0, 60))
        self.tb_tittle_label.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        self.tb_tittle_label.setFont(font)
        self.tb_tittle_label.setStyleSheet("background: transparent; color: white;")
        self.tb_tittle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tb_tittle_label.setObjectName("tb_tittle_label")
        self.leds_slider_header_layout_2.addWidget(self.tb_tittle_label)
        spacerItem20 = QtWidgets.QSpacerItem(
            0,
            60,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.leds_slider_header_layout_2.addItem(spacerItem20)
        self.tb_back_btn = IconButton(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_back_btn.sizePolicy().hasHeightForWidth())
        self.tb_back_btn.setSizePolicy(sizePolicy)
        self.tb_back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.tb_back_btn.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Momcake")
        font.setPointSize(24)
        font.setItalic(False)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.tb_back_btn.setFont(font)
        self.tb_back_btn.setMouseTracking(False)
        self.tb_back_btn.setTabletTracking(True)
        self.tb_back_btn.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.tb_back_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tb_back_btn.setStyleSheet("")
        self.tb_back_btn.setAutoDefault(False)
        self.tb_back_btn.setFlat(True)
        self.tb_back_btn.setProperty(
            "icon_pixmap", QtGui.QPixmap(":/ui/media/btn_icons/back.svg")
        )
        self.tb_back_btn.setObjectName("tb_back_btn")
        self.leds_slider_header_layout_2.addWidget(self.tb_back_btn)
        self.verticalLayout.addLayout(self.leds_slider_header_layout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel("idk whar to type this", parent=self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_10)
        self.verticalLayout.addLayout(None)
    
    xǁTroubleshootPageǁ_setupUI__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁTroubleshootPageǁ_setupUI__mutmut_1': xǁTroubleshootPageǁ_setupUI__mutmut_1, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_2': xǁTroubleshootPageǁ_setupUI__mutmut_2, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_3': xǁTroubleshootPageǁ_setupUI__mutmut_3, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_4': xǁTroubleshootPageǁ_setupUI__mutmut_4, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_5': xǁTroubleshootPageǁ_setupUI__mutmut_5, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_6': xǁTroubleshootPageǁ_setupUI__mutmut_6, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_7': xǁTroubleshootPageǁ_setupUI__mutmut_7, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_8': xǁTroubleshootPageǁ_setupUI__mutmut_8, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_9': xǁTroubleshootPageǁ_setupUI__mutmut_9, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_10': xǁTroubleshootPageǁ_setupUI__mutmut_10, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_11': xǁTroubleshootPageǁ_setupUI__mutmut_11, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_12': xǁTroubleshootPageǁ_setupUI__mutmut_12, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_13': xǁTroubleshootPageǁ_setupUI__mutmut_13, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_14': xǁTroubleshootPageǁ_setupUI__mutmut_14, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_15': xǁTroubleshootPageǁ_setupUI__mutmut_15, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_16': xǁTroubleshootPageǁ_setupUI__mutmut_16, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_17': xǁTroubleshootPageǁ_setupUI__mutmut_17, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_18': xǁTroubleshootPageǁ_setupUI__mutmut_18, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_19': xǁTroubleshootPageǁ_setupUI__mutmut_19, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_20': xǁTroubleshootPageǁ_setupUI__mutmut_20, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_21': xǁTroubleshootPageǁ_setupUI__mutmut_21, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_22': xǁTroubleshootPageǁ_setupUI__mutmut_22, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_23': xǁTroubleshootPageǁ_setupUI__mutmut_23, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_24': xǁTroubleshootPageǁ_setupUI__mutmut_24, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_25': xǁTroubleshootPageǁ_setupUI__mutmut_25, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_26': xǁTroubleshootPageǁ_setupUI__mutmut_26, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_27': xǁTroubleshootPageǁ_setupUI__mutmut_27, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_28': xǁTroubleshootPageǁ_setupUI__mutmut_28, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_29': xǁTroubleshootPageǁ_setupUI__mutmut_29, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_30': xǁTroubleshootPageǁ_setupUI__mutmut_30, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_31': xǁTroubleshootPageǁ_setupUI__mutmut_31, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_32': xǁTroubleshootPageǁ_setupUI__mutmut_32, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_33': xǁTroubleshootPageǁ_setupUI__mutmut_33, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_34': xǁTroubleshootPageǁ_setupUI__mutmut_34, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_35': xǁTroubleshootPageǁ_setupUI__mutmut_35, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_36': xǁTroubleshootPageǁ_setupUI__mutmut_36, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_37': xǁTroubleshootPageǁ_setupUI__mutmut_37, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_38': xǁTroubleshootPageǁ_setupUI__mutmut_38, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_39': xǁTroubleshootPageǁ_setupUI__mutmut_39, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_40': xǁTroubleshootPageǁ_setupUI__mutmut_40, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_41': xǁTroubleshootPageǁ_setupUI__mutmut_41, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_42': xǁTroubleshootPageǁ_setupUI__mutmut_42, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_43': xǁTroubleshootPageǁ_setupUI__mutmut_43, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_44': xǁTroubleshootPageǁ_setupUI__mutmut_44, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_45': xǁTroubleshootPageǁ_setupUI__mutmut_45, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_46': xǁTroubleshootPageǁ_setupUI__mutmut_46, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_47': xǁTroubleshootPageǁ_setupUI__mutmut_47, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_48': xǁTroubleshootPageǁ_setupUI__mutmut_48, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_49': xǁTroubleshootPageǁ_setupUI__mutmut_49, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_50': xǁTroubleshootPageǁ_setupUI__mutmut_50, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_51': xǁTroubleshootPageǁ_setupUI__mutmut_51, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_52': xǁTroubleshootPageǁ_setupUI__mutmut_52, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_53': xǁTroubleshootPageǁ_setupUI__mutmut_53, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_54': xǁTroubleshootPageǁ_setupUI__mutmut_54, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_55': xǁTroubleshootPageǁ_setupUI__mutmut_55, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_56': xǁTroubleshootPageǁ_setupUI__mutmut_56, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_57': xǁTroubleshootPageǁ_setupUI__mutmut_57, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_58': xǁTroubleshootPageǁ_setupUI__mutmut_58, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_59': xǁTroubleshootPageǁ_setupUI__mutmut_59, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_60': xǁTroubleshootPageǁ_setupUI__mutmut_60, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_61': xǁTroubleshootPageǁ_setupUI__mutmut_61, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_62': xǁTroubleshootPageǁ_setupUI__mutmut_62, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_63': xǁTroubleshootPageǁ_setupUI__mutmut_63, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_64': xǁTroubleshootPageǁ_setupUI__mutmut_64, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_65': xǁTroubleshootPageǁ_setupUI__mutmut_65, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_66': xǁTroubleshootPageǁ_setupUI__mutmut_66, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_67': xǁTroubleshootPageǁ_setupUI__mutmut_67, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_68': xǁTroubleshootPageǁ_setupUI__mutmut_68, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_69': xǁTroubleshootPageǁ_setupUI__mutmut_69, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_70': xǁTroubleshootPageǁ_setupUI__mutmut_70, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_71': xǁTroubleshootPageǁ_setupUI__mutmut_71, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_72': xǁTroubleshootPageǁ_setupUI__mutmut_72, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_73': xǁTroubleshootPageǁ_setupUI__mutmut_73, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_74': xǁTroubleshootPageǁ_setupUI__mutmut_74, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_75': xǁTroubleshootPageǁ_setupUI__mutmut_75, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_76': xǁTroubleshootPageǁ_setupUI__mutmut_76, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_77': xǁTroubleshootPageǁ_setupUI__mutmut_77, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_78': xǁTroubleshootPageǁ_setupUI__mutmut_78, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_79': xǁTroubleshootPageǁ_setupUI__mutmut_79, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_80': xǁTroubleshootPageǁ_setupUI__mutmut_80, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_81': xǁTroubleshootPageǁ_setupUI__mutmut_81, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_82': xǁTroubleshootPageǁ_setupUI__mutmut_82, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_83': xǁTroubleshootPageǁ_setupUI__mutmut_83, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_84': xǁTroubleshootPageǁ_setupUI__mutmut_84, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_85': xǁTroubleshootPageǁ_setupUI__mutmut_85, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_86': xǁTroubleshootPageǁ_setupUI__mutmut_86, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_87': xǁTroubleshootPageǁ_setupUI__mutmut_87, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_88': xǁTroubleshootPageǁ_setupUI__mutmut_88, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_89': xǁTroubleshootPageǁ_setupUI__mutmut_89, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_90': xǁTroubleshootPageǁ_setupUI__mutmut_90, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_91': xǁTroubleshootPageǁ_setupUI__mutmut_91, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_92': xǁTroubleshootPageǁ_setupUI__mutmut_92, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_93': xǁTroubleshootPageǁ_setupUI__mutmut_93, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_94': xǁTroubleshootPageǁ_setupUI__mutmut_94, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_95': xǁTroubleshootPageǁ_setupUI__mutmut_95, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_96': xǁTroubleshootPageǁ_setupUI__mutmut_96, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_97': xǁTroubleshootPageǁ_setupUI__mutmut_97, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_98': xǁTroubleshootPageǁ_setupUI__mutmut_98, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_99': xǁTroubleshootPageǁ_setupUI__mutmut_99, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_100': xǁTroubleshootPageǁ_setupUI__mutmut_100, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_101': xǁTroubleshootPageǁ_setupUI__mutmut_101, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_102': xǁTroubleshootPageǁ_setupUI__mutmut_102, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_103': xǁTroubleshootPageǁ_setupUI__mutmut_103, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_104': xǁTroubleshootPageǁ_setupUI__mutmut_104, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_105': xǁTroubleshootPageǁ_setupUI__mutmut_105, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_106': xǁTroubleshootPageǁ_setupUI__mutmut_106, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_107': xǁTroubleshootPageǁ_setupUI__mutmut_107, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_108': xǁTroubleshootPageǁ_setupUI__mutmut_108, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_109': xǁTroubleshootPageǁ_setupUI__mutmut_109, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_110': xǁTroubleshootPageǁ_setupUI__mutmut_110, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_111': xǁTroubleshootPageǁ_setupUI__mutmut_111, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_112': xǁTroubleshootPageǁ_setupUI__mutmut_112, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_113': xǁTroubleshootPageǁ_setupUI__mutmut_113, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_114': xǁTroubleshootPageǁ_setupUI__mutmut_114, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_115': xǁTroubleshootPageǁ_setupUI__mutmut_115, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_116': xǁTroubleshootPageǁ_setupUI__mutmut_116, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_117': xǁTroubleshootPageǁ_setupUI__mutmut_117, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_118': xǁTroubleshootPageǁ_setupUI__mutmut_118, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_119': xǁTroubleshootPageǁ_setupUI__mutmut_119, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_120': xǁTroubleshootPageǁ_setupUI__mutmut_120, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_121': xǁTroubleshootPageǁ_setupUI__mutmut_121, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_122': xǁTroubleshootPageǁ_setupUI__mutmut_122, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_123': xǁTroubleshootPageǁ_setupUI__mutmut_123, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_124': xǁTroubleshootPageǁ_setupUI__mutmut_124, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_125': xǁTroubleshootPageǁ_setupUI__mutmut_125, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_126': xǁTroubleshootPageǁ_setupUI__mutmut_126, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_127': xǁTroubleshootPageǁ_setupUI__mutmut_127, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_128': xǁTroubleshootPageǁ_setupUI__mutmut_128, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_129': xǁTroubleshootPageǁ_setupUI__mutmut_129, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_130': xǁTroubleshootPageǁ_setupUI__mutmut_130, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_131': xǁTroubleshootPageǁ_setupUI__mutmut_131, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_132': xǁTroubleshootPageǁ_setupUI__mutmut_132, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_133': xǁTroubleshootPageǁ_setupUI__mutmut_133, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_134': xǁTroubleshootPageǁ_setupUI__mutmut_134, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_135': xǁTroubleshootPageǁ_setupUI__mutmut_135, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_136': xǁTroubleshootPageǁ_setupUI__mutmut_136, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_137': xǁTroubleshootPageǁ_setupUI__mutmut_137, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_138': xǁTroubleshootPageǁ_setupUI__mutmut_138, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_139': xǁTroubleshootPageǁ_setupUI__mutmut_139, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_140': xǁTroubleshootPageǁ_setupUI__mutmut_140, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_141': xǁTroubleshootPageǁ_setupUI__mutmut_141, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_142': xǁTroubleshootPageǁ_setupUI__mutmut_142, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_143': xǁTroubleshootPageǁ_setupUI__mutmut_143, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_144': xǁTroubleshootPageǁ_setupUI__mutmut_144, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_145': xǁTroubleshootPageǁ_setupUI__mutmut_145, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_146': xǁTroubleshootPageǁ_setupUI__mutmut_146, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_147': xǁTroubleshootPageǁ_setupUI__mutmut_147, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_148': xǁTroubleshootPageǁ_setupUI__mutmut_148, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_149': xǁTroubleshootPageǁ_setupUI__mutmut_149, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_150': xǁTroubleshootPageǁ_setupUI__mutmut_150, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_151': xǁTroubleshootPageǁ_setupUI__mutmut_151, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_152': xǁTroubleshootPageǁ_setupUI__mutmut_152, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_153': xǁTroubleshootPageǁ_setupUI__mutmut_153, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_154': xǁTroubleshootPageǁ_setupUI__mutmut_154, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_155': xǁTroubleshootPageǁ_setupUI__mutmut_155, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_156': xǁTroubleshootPageǁ_setupUI__mutmut_156, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_157': xǁTroubleshootPageǁ_setupUI__mutmut_157, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_158': xǁTroubleshootPageǁ_setupUI__mutmut_158, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_159': xǁTroubleshootPageǁ_setupUI__mutmut_159, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_160': xǁTroubleshootPageǁ_setupUI__mutmut_160, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_161': xǁTroubleshootPageǁ_setupUI__mutmut_161, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_162': xǁTroubleshootPageǁ_setupUI__mutmut_162, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_163': xǁTroubleshootPageǁ_setupUI__mutmut_163, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_164': xǁTroubleshootPageǁ_setupUI__mutmut_164, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_165': xǁTroubleshootPageǁ_setupUI__mutmut_165, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_166': xǁTroubleshootPageǁ_setupUI__mutmut_166, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_167': xǁTroubleshootPageǁ_setupUI__mutmut_167, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_168': xǁTroubleshootPageǁ_setupUI__mutmut_168, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_169': xǁTroubleshootPageǁ_setupUI__mutmut_169, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_170': xǁTroubleshootPageǁ_setupUI__mutmut_170, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_171': xǁTroubleshootPageǁ_setupUI__mutmut_171, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_172': xǁTroubleshootPageǁ_setupUI__mutmut_172, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_173': xǁTroubleshootPageǁ_setupUI__mutmut_173, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_174': xǁTroubleshootPageǁ_setupUI__mutmut_174, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_175': xǁTroubleshootPageǁ_setupUI__mutmut_175, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_176': xǁTroubleshootPageǁ_setupUI__mutmut_176, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_177': xǁTroubleshootPageǁ_setupUI__mutmut_177, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_178': xǁTroubleshootPageǁ_setupUI__mutmut_178, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_179': xǁTroubleshootPageǁ_setupUI__mutmut_179, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_180': xǁTroubleshootPageǁ_setupUI__mutmut_180, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_181': xǁTroubleshootPageǁ_setupUI__mutmut_181, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_182': xǁTroubleshootPageǁ_setupUI__mutmut_182, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_183': xǁTroubleshootPageǁ_setupUI__mutmut_183, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_184': xǁTroubleshootPageǁ_setupUI__mutmut_184, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_185': xǁTroubleshootPageǁ_setupUI__mutmut_185, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_186': xǁTroubleshootPageǁ_setupUI__mutmut_186, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_187': xǁTroubleshootPageǁ_setupUI__mutmut_187, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_188': xǁTroubleshootPageǁ_setupUI__mutmut_188, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_189': xǁTroubleshootPageǁ_setupUI__mutmut_189, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_190': xǁTroubleshootPageǁ_setupUI__mutmut_190, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_191': xǁTroubleshootPageǁ_setupUI__mutmut_191, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_192': xǁTroubleshootPageǁ_setupUI__mutmut_192, 
        'xǁTroubleshootPageǁ_setupUI__mutmut_193': xǁTroubleshootPageǁ_setupUI__mutmut_193
    }
    xǁTroubleshootPageǁ_setupUI__mutmut_orig.__name__ = 'xǁTroubleshootPageǁ_setupUI'
