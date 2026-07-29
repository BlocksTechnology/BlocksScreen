import helper_methods as helper_methods
from PyQt6 import QtCore, QtWidgets
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


class ScreenSaver(QtCore.QObject):
    timer = QtCore.QTimer()
    dpms_off_timeout = helper_methods.get_dpms_timeouts().get("off_timeout")
    dpms_suspend_timeout = helper_methods.get_dpms_timeouts().get("suspend_timeout")
    dpms_standby_timeout = helper_methods.get_dpms_timeouts().get("standby_timeout")
    touch_blocked: bool = False

    def __init__(self, parent) -> None:
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁScreenSaverǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁScreenSaverǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁScreenSaverǁ__init____mutmut_orig(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_1(self, parent) -> None:
        super().__init__()

        self.screensaver_config = None
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_2(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            None, fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_3(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_4(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_5(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "XXscreensaverXX", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_6(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "SCREENSAVER", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_7(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_8(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = None
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_9(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900001
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_10(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = None
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_11(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                None, default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_12(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=None
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_13(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_14(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_15(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "XXtimeoutXX", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_16(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "TIMEOUT", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_17(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500001
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_18(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(None)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_19(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(None)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def xǁScreenSaverǁ__init____mutmut_20(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout if self.dpms_standby_timeout else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(None)
        self.timer.start()
    
    xǁScreenSaverǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁScreenSaverǁ__init____mutmut_1': xǁScreenSaverǁ__init____mutmut_1, 
        'xǁScreenSaverǁ__init____mutmut_2': xǁScreenSaverǁ__init____mutmut_2, 
        'xǁScreenSaverǁ__init____mutmut_3': xǁScreenSaverǁ__init____mutmut_3, 
        'xǁScreenSaverǁ__init____mutmut_4': xǁScreenSaverǁ__init____mutmut_4, 
        'xǁScreenSaverǁ__init____mutmut_5': xǁScreenSaverǁ__init____mutmut_5, 
        'xǁScreenSaverǁ__init____mutmut_6': xǁScreenSaverǁ__init____mutmut_6, 
        'xǁScreenSaverǁ__init____mutmut_7': xǁScreenSaverǁ__init____mutmut_7, 
        'xǁScreenSaverǁ__init____mutmut_8': xǁScreenSaverǁ__init____mutmut_8, 
        'xǁScreenSaverǁ__init____mutmut_9': xǁScreenSaverǁ__init____mutmut_9, 
        'xǁScreenSaverǁ__init____mutmut_10': xǁScreenSaverǁ__init____mutmut_10, 
        'xǁScreenSaverǁ__init____mutmut_11': xǁScreenSaverǁ__init____mutmut_11, 
        'xǁScreenSaverǁ__init____mutmut_12': xǁScreenSaverǁ__init____mutmut_12, 
        'xǁScreenSaverǁ__init____mutmut_13': xǁScreenSaverǁ__init____mutmut_13, 
        'xǁScreenSaverǁ__init____mutmut_14': xǁScreenSaverǁ__init____mutmut_14, 
        'xǁScreenSaverǁ__init____mutmut_15': xǁScreenSaverǁ__init____mutmut_15, 
        'xǁScreenSaverǁ__init____mutmut_16': xǁScreenSaverǁ__init____mutmut_16, 
        'xǁScreenSaverǁ__init____mutmut_17': xǁScreenSaverǁ__init____mutmut_17, 
        'xǁScreenSaverǁ__init____mutmut_18': xǁScreenSaverǁ__init____mutmut_18, 
        'xǁScreenSaverǁ__init____mutmut_19': xǁScreenSaverǁ__init____mutmut_19, 
        'xǁScreenSaverǁ__init____mutmut_20': xǁScreenSaverǁ__init____mutmut_20
    }
    xǁScreenSaverǁ__init____mutmut_orig.__name__ = 'xǁScreenSaverǁ__init__'

    def eventFilter(self, object, event) -> bool:
        args = [object, event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁScreenSaverǁeventFilter__mutmut_orig'), object.__getattribute__(self, 'xǁScreenSaverǁeventFilter__mutmut_mutants'), args, kwargs, self)

    def xǁScreenSaverǁeventFilter__mutmut_orig(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_1(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() not in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_2(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = None
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_3(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                ) and self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_4(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get(None)
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_5(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("XXstateXX")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_6(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("STATE")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_7(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state") not in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_8(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_9(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = None
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_10(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = True
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_11(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(None)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_12(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return False  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def xǁScreenSaverǁeventFilter__mutmut_13(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            dpms_info = helper_methods.get_dpms_info()
            if (
                dpms_info.get("state")
                in (
                    helper_methods.DPMSState.OFF,
                    helper_methods.DPMSState.STANDBY,
                    helper_methods.DPMSState.SUSPEND,
                )
                or self.touch_blocked
            ):
                if not self.timer.isActive():
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
            else:
                self.timer.stop()
                self.timer.start()
        return True
    
    xǁScreenSaverǁeventFilter__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁScreenSaverǁeventFilter__mutmut_1': xǁScreenSaverǁeventFilter__mutmut_1, 
        'xǁScreenSaverǁeventFilter__mutmut_2': xǁScreenSaverǁeventFilter__mutmut_2, 
        'xǁScreenSaverǁeventFilter__mutmut_3': xǁScreenSaverǁeventFilter__mutmut_3, 
        'xǁScreenSaverǁeventFilter__mutmut_4': xǁScreenSaverǁeventFilter__mutmut_4, 
        'xǁScreenSaverǁeventFilter__mutmut_5': xǁScreenSaverǁeventFilter__mutmut_5, 
        'xǁScreenSaverǁeventFilter__mutmut_6': xǁScreenSaverǁeventFilter__mutmut_6, 
        'xǁScreenSaverǁeventFilter__mutmut_7': xǁScreenSaverǁeventFilter__mutmut_7, 
        'xǁScreenSaverǁeventFilter__mutmut_8': xǁScreenSaverǁeventFilter__mutmut_8, 
        'xǁScreenSaverǁeventFilter__mutmut_9': xǁScreenSaverǁeventFilter__mutmut_9, 
        'xǁScreenSaverǁeventFilter__mutmut_10': xǁScreenSaverǁeventFilter__mutmut_10, 
        'xǁScreenSaverǁeventFilter__mutmut_11': xǁScreenSaverǁeventFilter__mutmut_11, 
        'xǁScreenSaverǁeventFilter__mutmut_12': xǁScreenSaverǁeventFilter__mutmut_12, 
        'xǁScreenSaverǁeventFilter__mutmut_13': xǁScreenSaverǁeventFilter__mutmut_13
    }
    xǁScreenSaverǁeventFilter__mutmut_orig.__name__ = 'xǁScreenSaverǁeventFilter'

    def check_dpms(self) -> None:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁScreenSaverǁcheck_dpms__mutmut_orig'), object.__getattribute__(self, 'xǁScreenSaverǁcheck_dpms__mutmut_mutants'), args, kwargs, self)

    def xǁScreenSaverǁcheck_dpms__mutmut_orig(self) -> None:
        """Checks the X11 extension dpms for the status of the screen"""
        self.touch_blocked = True
        helper_methods.set_dpms_mode(helper_methods.DPMSState.STANDBY)
        self.timer.stop()

    def xǁScreenSaverǁcheck_dpms__mutmut_1(self) -> None:
        """Checks the X11 extension dpms for the status of the screen"""
        self.touch_blocked = None
        helper_methods.set_dpms_mode(helper_methods.DPMSState.STANDBY)
        self.timer.stop()

    def xǁScreenSaverǁcheck_dpms__mutmut_2(self) -> None:
        """Checks the X11 extension dpms for the status of the screen"""
        self.touch_blocked = False
        helper_methods.set_dpms_mode(helper_methods.DPMSState.STANDBY)
        self.timer.stop()

    def xǁScreenSaverǁcheck_dpms__mutmut_3(self) -> None:
        """Checks the X11 extension dpms for the status of the screen"""
        self.touch_blocked = True
        helper_methods.set_dpms_mode(None)
        self.timer.stop()
    
    xǁScreenSaverǁcheck_dpms__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁScreenSaverǁcheck_dpms__mutmut_1': xǁScreenSaverǁcheck_dpms__mutmut_1, 
        'xǁScreenSaverǁcheck_dpms__mutmut_2': xǁScreenSaverǁcheck_dpms__mutmut_2, 
        'xǁScreenSaverǁcheck_dpms__mutmut_3': xǁScreenSaverǁcheck_dpms__mutmut_3
    }
    xǁScreenSaverǁcheck_dpms__mutmut_orig.__name__ = 'xǁScreenSaverǁcheck_dpms'
