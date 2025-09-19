import helper_methods as helper_methods
from PyQt6 import QtCore, QtWidgets ,QtGui
import typing

class ScreenSaver(QtCore.QObject):
    timer = QtCore.QTimer()
    dpms_off_timeout = helper_methods.get_dpms_timeouts().get("off_timeout")
    dpms_suspend_timeout = helper_methods.get_dpms_timeouts().get(
        "suspend_timeout"
    )
    dpms_standby_timeout = helper_methods.get_dpms_timeouts().get(
        "standby_timeout"
    )
    request_file_info: typing.ClassVar[QtCore.pyqtSignal] = QtCore.pyqtSignal(
        str, name="request_file_info"
     )


    touch_blocked: bool = False

    def __init__(self, parent) -> None:
        super().__init__()

        self.screensaver_config = parent.config.get_section(
            "screensaver", fallback=None
        )
        if not self.screensaver_config:
            self.blank_timeout = (
                self.dpms_standby_timeout
                if self.dpms_standby_timeout
                else 900000
            )
        else:
            self.blank_timeout = self.screensaver_config.getint(
                "timeout", default=500000
            )
        self.image_widget = QtWidgets.QLabel()
        self.image_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_widget.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.image=QtGui.QPixmap("BlocksScreen/lib/ui/resources/media/logoblocks.png")

        self.image_widget.setStyleSheet("background-color: black;")
        self.image_widget.setScaledContents(True)

        # load image from config or hardcode
        
        QtWidgets.QApplication.instance().installEventFilter(self)

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
            QtCore.QEvent.Type.MouseButtonDblClick,
        ):
            if self.image_widget.isVisible() or self.touch_blocked:
                self.touch_blocked = False
                self.image_widget.hide()
                self.timer.start()
                return True  # block the wake-up touch
        return False

    def timerEvent(self, a0: QtCore.QTimerEvent) -> None:
        return super().timerEvent(a0)

    def check_dpms(self) -> None:
        """Checks the X11 extension dpms for the status of the screen"""
        self.touch_blocked = True
        if self.state == "printing":
            self.request_file_info.emit(self.filename)
            self.image = QtGui.QPixmap(self.thumbnail[2])
        self.image_widget.setPixmap(self.image)
        self.image_widget.setMaximumWidth(self.image.width())
        self.image_widget.showFullScreen()
        self.timer.stop()
    
    @QtCore.pyqtSlot(dict, name="on_fileinfo")
    def on_fileinfo(self, filedata: dict) -> None:
        self.thumbnail = filedata["thumbnail_images"]


    @QtCore.pyqtSlot(str, dict, name="on_object_config")
    @QtCore.pyqtSlot(str, float, name="on_object_config")
    @QtCore.pyqtSlot(str, str, name="on_object_config")
    def on_object_config(self, field: str, value: dict | float | str) -> None:
        if field == "filename":
            self.filename = value
        if field == "state":
            self.state = value
            print(self.state)