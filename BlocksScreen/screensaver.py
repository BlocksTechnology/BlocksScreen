import os
import typing

import helper_methods as helper_methods
from PyQt6 import QtCore, QtWidgets


class ScreenSaver(QtCore.QObject):
    timer = QtCore.QTimer()

    dpms_off_timeout = helper_methods.get_dpms_timeouts().get("off_timeout")
    dpms_suspend_timeout = helper_methods.get_dpms_timeouts().get(
        "suspend_timeout"
    )
    dpms_standby_timeout = helper_methods.get_dpms_timeouts().get(
        "standby_timeout"
    )

    touch_blocked: bool = False

    def __init__(self) -> None:
        super().__init__()
        # Install event filters
        QtWidgets.QApplication.instance().installEventFilter(self)
        self.blank_timeout = (
            self.dpms_standby_timeout if self.dpms_standby_timeout else 6000
        )
        self.timer.timeout.connect(self.check_dpms)
        self.timer.setInterval(self.blank_timeout)
        self.timer.start()

    def eventFilter(self, object, event) -> bool:
        """Filter touch events considering DPMS Screen state"""

        if event.type() in (  # Block Touch Filter and Wake Touch Filter
            QtCore.QEvent.Type.TouchBegin,
            QtCore.QEvent.Type.TouchUpdate,
            QtCore.QEvent.Type.TouchEnd,
            QtCore.QEvent.Type.MouseButtonPress,
            # QtCore.QEvent.Type.MouseButtonRelease,
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
                    print("timer not active, starting")
                    self.touch_blocked = False
                    helper_methods.set_dpms_mode(helper_methods.DPMSState.ON)
                    self.timer.start()
                    return True  # filter out the event, block touch events on the application
        return False

    def timerEvent(self, a0: QtCore.QTimerEvent) -> None:
        return super().timerEvent(a0)

    def check_dpms(self) -> None:
        """Checks the X11 extension dpms for the status of the screen"""
        self.touch_blocked = True
        self.timer.stop()
