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


class NotificationTabBar(QtWidgets.QTabBar):
    """Re-implemented QTabBar so that the widget can have notifications"""

    def __init__(self, parent=None):
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNotificationTabBarǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁNotificationTabBarǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁNotificationTabBarǁ__init____mutmut_orig(self, parent=None):
        super().__init__(parent)
        self._notifications = {}  # {tab_index: bool}

    def xǁNotificationTabBarǁ__init____mutmut_1(self, parent=None):
        super().__init__(None)
        self._notifications = {}  # {tab_index: bool}

    def xǁNotificationTabBarǁ__init____mutmut_2(self, parent=None):
        super().__init__(parent)
        self._notifications = None  # {tab_index: bool}
    
    xǁNotificationTabBarǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNotificationTabBarǁ__init____mutmut_1': xǁNotificationTabBarǁ__init____mutmut_1, 
        'xǁNotificationTabBarǁ__init____mutmut_2': xǁNotificationTabBarǁ__init____mutmut_2
    }
    xǁNotificationTabBarǁ__init____mutmut_orig.__name__ = 'xǁNotificationTabBarǁ__init__'

    def setNotification(self, index: int, show: bool):
        args = [index, show]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNotificationTabBarǁsetNotification__mutmut_orig'), object.__getattribute__(self, 'xǁNotificationTabBarǁsetNotification__mutmut_mutants'), args, kwargs, self)

    def xǁNotificationTabBarǁsetNotification__mutmut_orig(self, index: int, show: bool):
        """Set notification"""
        if index < 0 or index >= self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(index))  # repaint only that tab

    def xǁNotificationTabBarǁsetNotification__mutmut_1(self, index: int, show: bool):
        """Set notification"""
        if index < 0 and index >= self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(index))  # repaint only that tab

    def xǁNotificationTabBarǁsetNotification__mutmut_2(self, index: int, show: bool):
        """Set notification"""
        if index <= 0 or index >= self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(index))  # repaint only that tab

    def xǁNotificationTabBarǁsetNotification__mutmut_3(self, index: int, show: bool):
        """Set notification"""
        if index < 1 or index >= self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(index))  # repaint only that tab

    def xǁNotificationTabBarǁsetNotification__mutmut_4(self, index: int, show: bool):
        """Set notification"""
        if index < 0 or index > self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(index))  # repaint only that tab

    def xǁNotificationTabBarǁsetNotification__mutmut_5(self, index: int, show: bool):
        """Set notification"""
        if index < 0 or index >= self.count():
            return
        self._notifications[index] = None
        self.update(self.tabRect(index))  # repaint only that tab

    def xǁNotificationTabBarǁsetNotification__mutmut_6(self, index: int, show: bool):
        """Set notification"""
        if index < 0 or index >= self.count():
            return
        self._notifications[index] = show
        self.update(None)  # repaint only that tab

    def xǁNotificationTabBarǁsetNotification__mutmut_7(self, index: int, show: bool):
        """Set notification"""
        if index < 0 or index >= self.count():
            return
        self._notifications[index] = show
        self.update(self.tabRect(None))  # repaint only that tab
    
    xǁNotificationTabBarǁsetNotification__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNotificationTabBarǁsetNotification__mutmut_1': xǁNotificationTabBarǁsetNotification__mutmut_1, 
        'xǁNotificationTabBarǁsetNotification__mutmut_2': xǁNotificationTabBarǁsetNotification__mutmut_2, 
        'xǁNotificationTabBarǁsetNotification__mutmut_3': xǁNotificationTabBarǁsetNotification__mutmut_3, 
        'xǁNotificationTabBarǁsetNotification__mutmut_4': xǁNotificationTabBarǁsetNotification__mutmut_4, 
        'xǁNotificationTabBarǁsetNotification__mutmut_5': xǁNotificationTabBarǁsetNotification__mutmut_5, 
        'xǁNotificationTabBarǁsetNotification__mutmut_6': xǁNotificationTabBarǁsetNotification__mutmut_6, 
        'xǁNotificationTabBarǁsetNotification__mutmut_7': xǁNotificationTabBarǁsetNotification__mutmut_7
    }
    xǁNotificationTabBarǁsetNotification__mutmut_orig.__name__ = 'xǁNotificationTabBarǁsetNotification'

    def paintEvent(self, event):
        args = [event]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNotificationTabBarǁpaintEvent__mutmut_orig'), object.__getattribute__(self, 'xǁNotificationTabBarǁpaintEvent__mutmut_mutants'), args, kwargs, self)

    def xǁNotificationTabBarǁpaintEvent__mutmut_orig(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_1(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(None)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_2(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = None
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_3(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(None)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_4(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(None)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_5(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(None):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_6(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(None, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_7(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, None):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_8(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_9(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, ):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_10(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, True):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_11(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = None
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_12(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(None)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_13(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = None
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_14(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(None, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_15(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, None)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_16(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_17(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, )
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_18(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(11, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_19(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() / 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_20(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 1.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_21(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = None
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_22(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter + 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_23(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() + dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_24(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 5
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_25(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = None
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_26(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() - 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_27(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 31
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_28(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(None)
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_29(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(None, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_30(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, None, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_31(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, None))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_32(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_33(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_34(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, ))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_35(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(227, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_36(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 32, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_37(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 32))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_38(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(None)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_39(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    None, dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_40(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), None, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_41(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, None, int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_42(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), None
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_43(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_44(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_45(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_46(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), )

    def xǁNotificationTabBarǁpaintEvent__mutmut_47(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(None), dot_y, int(dot_diameter), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_48(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(None), int(dot_diameter)
                )

    def xǁNotificationTabBarǁpaintEvent__mutmut_49(self, event):
        """Re-implemented method, paint widget"""
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            if self._notifications.get(i, False):
                rect = self.tabRect(i)
                dot_diameter = min(10, rect.height() * 0.3)
                dot_x = rect.right() - dot_diameter - 4
                dot_y = rect.top() + 30
                painter.setBrush(QtGui.QColor(226, 31, 31))
                painter.setPen(QtCore.Qt.PenStyle.NoPen)
                painter.drawEllipse(
                    int(dot_x), dot_y, int(dot_diameter), int(None)
                )
    
    xǁNotificationTabBarǁpaintEvent__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNotificationTabBarǁpaintEvent__mutmut_1': xǁNotificationTabBarǁpaintEvent__mutmut_1, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_2': xǁNotificationTabBarǁpaintEvent__mutmut_2, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_3': xǁNotificationTabBarǁpaintEvent__mutmut_3, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_4': xǁNotificationTabBarǁpaintEvent__mutmut_4, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_5': xǁNotificationTabBarǁpaintEvent__mutmut_5, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_6': xǁNotificationTabBarǁpaintEvent__mutmut_6, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_7': xǁNotificationTabBarǁpaintEvent__mutmut_7, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_8': xǁNotificationTabBarǁpaintEvent__mutmut_8, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_9': xǁNotificationTabBarǁpaintEvent__mutmut_9, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_10': xǁNotificationTabBarǁpaintEvent__mutmut_10, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_11': xǁNotificationTabBarǁpaintEvent__mutmut_11, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_12': xǁNotificationTabBarǁpaintEvent__mutmut_12, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_13': xǁNotificationTabBarǁpaintEvent__mutmut_13, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_14': xǁNotificationTabBarǁpaintEvent__mutmut_14, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_15': xǁNotificationTabBarǁpaintEvent__mutmut_15, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_16': xǁNotificationTabBarǁpaintEvent__mutmut_16, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_17': xǁNotificationTabBarǁpaintEvent__mutmut_17, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_18': xǁNotificationTabBarǁpaintEvent__mutmut_18, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_19': xǁNotificationTabBarǁpaintEvent__mutmut_19, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_20': xǁNotificationTabBarǁpaintEvent__mutmut_20, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_21': xǁNotificationTabBarǁpaintEvent__mutmut_21, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_22': xǁNotificationTabBarǁpaintEvent__mutmut_22, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_23': xǁNotificationTabBarǁpaintEvent__mutmut_23, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_24': xǁNotificationTabBarǁpaintEvent__mutmut_24, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_25': xǁNotificationTabBarǁpaintEvent__mutmut_25, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_26': xǁNotificationTabBarǁpaintEvent__mutmut_26, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_27': xǁNotificationTabBarǁpaintEvent__mutmut_27, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_28': xǁNotificationTabBarǁpaintEvent__mutmut_28, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_29': xǁNotificationTabBarǁpaintEvent__mutmut_29, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_30': xǁNotificationTabBarǁpaintEvent__mutmut_30, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_31': xǁNotificationTabBarǁpaintEvent__mutmut_31, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_32': xǁNotificationTabBarǁpaintEvent__mutmut_32, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_33': xǁNotificationTabBarǁpaintEvent__mutmut_33, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_34': xǁNotificationTabBarǁpaintEvent__mutmut_34, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_35': xǁNotificationTabBarǁpaintEvent__mutmut_35, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_36': xǁNotificationTabBarǁpaintEvent__mutmut_36, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_37': xǁNotificationTabBarǁpaintEvent__mutmut_37, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_38': xǁNotificationTabBarǁpaintEvent__mutmut_38, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_39': xǁNotificationTabBarǁpaintEvent__mutmut_39, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_40': xǁNotificationTabBarǁpaintEvent__mutmut_40, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_41': xǁNotificationTabBarǁpaintEvent__mutmut_41, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_42': xǁNotificationTabBarǁpaintEvent__mutmut_42, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_43': xǁNotificationTabBarǁpaintEvent__mutmut_43, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_44': xǁNotificationTabBarǁpaintEvent__mutmut_44, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_45': xǁNotificationTabBarǁpaintEvent__mutmut_45, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_46': xǁNotificationTabBarǁpaintEvent__mutmut_46, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_47': xǁNotificationTabBarǁpaintEvent__mutmut_47, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_48': xǁNotificationTabBarǁpaintEvent__mutmut_48, 
        'xǁNotificationTabBarǁpaintEvent__mutmut_49': xǁNotificationTabBarǁpaintEvent__mutmut_49
    }
    xǁNotificationTabBarǁpaintEvent__mutmut_orig.__name__ = 'xǁNotificationTabBarǁpaintEvent'


class NotificationQTabWidget(QtWidgets.QTabWidget):
    """Re-implemented QTabWidget so that we can have notifications"""

    def __init__(self, parent=None):
        args = [parent]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNotificationQTabWidgetǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁNotificationQTabWidgetǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁNotificationQTabWidgetǁ__init____mutmut_orig(self, parent=None):
        super().__init__(parent)
        self._custom_tabbar = NotificationTabBar()
        self.setTabBar(self._custom_tabbar)

    def xǁNotificationQTabWidgetǁ__init____mutmut_1(self, parent=None):
        super().__init__(None)
        self._custom_tabbar = NotificationTabBar()
        self.setTabBar(self._custom_tabbar)

    def xǁNotificationQTabWidgetǁ__init____mutmut_2(self, parent=None):
        super().__init__(parent)
        self._custom_tabbar = None
        self.setTabBar(self._custom_tabbar)

    def xǁNotificationQTabWidgetǁ__init____mutmut_3(self, parent=None):
        super().__init__(parent)
        self._custom_tabbar = NotificationTabBar()
        self.setTabBar(None)
    
    xǁNotificationQTabWidgetǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNotificationQTabWidgetǁ__init____mutmut_1': xǁNotificationQTabWidgetǁ__init____mutmut_1, 
        'xǁNotificationQTabWidgetǁ__init____mutmut_2': xǁNotificationQTabWidgetǁ__init____mutmut_2, 
        'xǁNotificationQTabWidgetǁ__init____mutmut_3': xǁNotificationQTabWidgetǁ__init____mutmut_3
    }
    xǁNotificationQTabWidgetǁ__init____mutmut_orig.__name__ = 'xǁNotificationQTabWidgetǁ__init__'

    def setNotification(self, index: int, show: bool):
        args = [index, show]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁNotificationQTabWidgetǁsetNotification__mutmut_orig'), object.__getattribute__(self, 'xǁNotificationQTabWidgetǁsetNotification__mutmut_mutants'), args, kwargs, self)

    def xǁNotificationQTabWidgetǁsetNotification__mutmut_orig(self, index: int, show: bool):
        """Set tab notification"""
        self._custom_tabbar.setNotification(index, show)

    def xǁNotificationQTabWidgetǁsetNotification__mutmut_1(self, index: int, show: bool):
        """Set tab notification"""
        self._custom_tabbar.setNotification(None, show)

    def xǁNotificationQTabWidgetǁsetNotification__mutmut_2(self, index: int, show: bool):
        """Set tab notification"""
        self._custom_tabbar.setNotification(index, None)

    def xǁNotificationQTabWidgetǁsetNotification__mutmut_3(self, index: int, show: bool):
        """Set tab notification"""
        self._custom_tabbar.setNotification(show)

    def xǁNotificationQTabWidgetǁsetNotification__mutmut_4(self, index: int, show: bool):
        """Set tab notification"""
        self._custom_tabbar.setNotification(index, )
    
    xǁNotificationQTabWidgetǁsetNotification__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁNotificationQTabWidgetǁsetNotification__mutmut_1': xǁNotificationQTabWidgetǁsetNotification__mutmut_1, 
        'xǁNotificationQTabWidgetǁsetNotification__mutmut_2': xǁNotificationQTabWidgetǁsetNotification__mutmut_2, 
        'xǁNotificationQTabWidgetǁsetNotification__mutmut_3': xǁNotificationQTabWidgetǁsetNotification__mutmut_3, 
        'xǁNotificationQTabWidgetǁsetNotification__mutmut_4': xǁNotificationQTabWidgetǁsetNotification__mutmut_4
    }
    xǁNotificationQTabWidgetǁsetNotification__mutmut_orig.__name__ = 'xǁNotificationQTabWidgetǁsetNotification'
