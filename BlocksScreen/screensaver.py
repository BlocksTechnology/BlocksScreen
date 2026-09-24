import helper_methods as helper_methods
from PyQt6 import QtCore, QtWidgets


class ScreenSaver(QtCore.QObject):
    """Screensaver that uses X11 DPMS to blank the display after inactivity."""

    timer = QtCore.QTimer()
    touch_blocked: bool = False
    _dpms_available: bool = hasattr(helper_methods, "get_dpms_timeouts")

    def __init__(self, parent) -> None:
        super().__init__()

        dpms_timeouts = (
            helper_methods.get_dpms_timeouts() if self._dpms_available else {}
        )
        self.dpms_off_timeout = dpms_timeouts.get("off_timeout")
        self.dpms_suspend_timeout = dpms_timeouts.get("suspend_timeout")
        self.dpms_standby_timeout = dpms_timeouts.get("standby_timeout")

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

    def eventFilter(self, object, event) -> bool:
        """Filter touch events considering DPMS screen state."""
        if not self._dpms_available:
            return False

        if event.type() in (
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
                    return True
            else:
                self.timer.stop()
                self.timer.start()
        return False

    def check_dpms(self) -> None:
        """Blank the display via DPMS standby."""
        self.touch_blocked = True
        if self._dpms_available:
            helper_methods.set_dpms_mode(helper_methods.DPMSState.STANDBY)
        self.timer.stop()
